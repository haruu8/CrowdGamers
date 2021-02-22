from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.views import generic
from teams.models import Question, UserProfile
from accounts.models import User



class HomeView(TemplateView):
    template_name = 'teams/home.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_anonymous:
            pass
        else:
            context = super().get_context_data(**kwargs)
            context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            return context

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

home = HomeView.as_view()



class FreqentlyQuestionAskedView(generic.TemplateView):
    template_name = 'teams/support/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Question.objects.all()
        return context

faq = FreqentlyQuestionAskedView.as_view()
