from django.views.generic import TemplateView
from teams.models import Question
from .utils import GetProfileView



class HomeView(GetProfileView):
    template_name='teams/home.html'

home = HomeView.as_view()



class ContactView(GetProfileView):
    template_name='teams/support/contact.html'

contact = ContactView.as_view()



class FreqentlyQuestionAskedView(GetProfileView):
    """
    よくある質問を一覧表示する
    """
    template_name = 'teams/support/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Question.objects.all()
        return context

faq = FreqentlyQuestionAskedView.as_view()



class TermsOfServiceView(TemplateView):
    template_name = 'teams/support/terms_of_service.html'

terms_of_service = TermsOfServiceView.as_view()



class PrivacyPolicyView(TemplateView):
    template_name = 'teams/support/privacy_policy.html'

privacy_policy = PrivacyPolicyView.as_view()
