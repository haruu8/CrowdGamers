from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.mixins import AccessMixin
from teams.models import UserProfile
from accounts.models import User



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser



class CustomAccessMixin(AccessMixin):
    """ handle_no_permission で違う処理を流したいため、そこだけ編集 """

    home_url = None

    def get_home_url(self):
        """
        このメソッドをオーバーライドして、 home_url属性をオーバーライドします。
        """
        home_url = self.home_url or settings.LOGIN_REDIRECT_URL
        if not home_url:
            raise ImproperlyConfigured(
                '{0} is missing the home_url attribute. Define {0}.home_url, settings.LOGIN_REDIRECT_URL, or override '
                '{0}.get_home_url().'.format(self.__class__.__name__)
            )
        # return str(home_url)
        return redirect(home_url)

    def handle_no_permission(self):
        if self.raise_exception or not self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return self.get_home_url()



class AnonymousRequiredMixin(CustomAccessMixin):
    """ リクエストユーザーがログインしていないことを確認 """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



class OnlyOwnerMixin(UserPassesTestMixin):
    pass
    # raise_exception = True

    # def test_func(self):
    #     return self.request.user.profile.is_owner == self.kwargs['username'] or self.request.user.is_superuser
