from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from teams.models import UserProfile
from accounts.models import User



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser



def anonymous_required( view_function, redirect_to = None ):
    return AnonymousRequired( view_function, redirect_to )



class AnonymousRequired(object):
    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect( self.redirect_to )
        return self.view_function( request, *args, **kwargs )



class OnlyOwnerMixin(UserPassesTestMixin):
    pass
    # raise_exception = True

    # def test_func(self):
    #     return self.request.user.profile.is_owner == self.kwargs['username'] or self.request.user.is_superuser
