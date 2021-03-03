from django.views.generic import TemplateView
from teams.models import Question
from .utils import GetProfileView
import markdown as md



# class FreqentlyQuestionAskedView(TemplateView):
class FreqentlyQuestionAskedView(GetProfileView):
    template_name = 'teams/support/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Question.objects.all()
        return context

faq = FreqentlyQuestionAskedView.as_view()



class TermsOfServiceView(GetProfileView):
    template_name = 'teams/support/terms_of_service.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['terms_of_service'] = Question.objects.all()
    #     return context

terms_of_service = TermsOfServiceView.as_view()



class PrivacyPolicyView(GetProfileView):
    template_name = 'teams/support/privacy_policy.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['privacy_policy'] = Question.objects.all()
    #     return context

privacy_policy = PrivacyPolicyView.as_view()
