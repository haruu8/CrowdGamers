from django.views.generic import TemplateView
from teams.models import Question



class FreqentlyQuestionAskedView(TemplateView):
    template_name = 'teams/support/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Question.objects.all()
        return context

faq = FreqentlyQuestionAskedView.as_view()
