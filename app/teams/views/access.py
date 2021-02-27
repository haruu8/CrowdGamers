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



class OnlyOwnerMixin(UserPassesTestMixin):
    pass
    # raise_exception = True

    # def test_func(self):
    #     return self.request.user.profile.is_owner == self.kwargs['username'] or self.request.user.is_superuser
