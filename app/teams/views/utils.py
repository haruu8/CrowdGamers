from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from teams.models import UserProfile
from accounts.models import User



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser



class AnonymousRequiredMixin(UserPassesTestMixin):
    pass


class GetProfileView(TemplateView):

    def get_context_data(self, **kwargs):
        if self.request.user.is_anonymous:
            pass
        else:
            context = super().get_context_data(**kwargs)
            context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            return context

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
