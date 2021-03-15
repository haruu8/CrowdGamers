from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth import get_user_model, views as auth_views, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from teams.views import OnlyYouMixin, AnonymousRequiredMixin



class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    """
    ログインする。
    """
    template_name = 'accounts/login.html'

login = LoginView.as_view()



class SignupView(AnonymousRequiredMixin, auth_views.LoginView):
    """
    サインアップする。
    """
    template_name = 'accounts/signup.html'

signup = SignupView.as_view()



class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """
    ログアウトする。
    """
    pass

logout = LoginView.as_view()



class UserDeleteView(OnlyYouMixin, LoginRequiredMixin, TemplateView):
    """
    ユーザーを削除する。

    Notes
    -----
    buttonを使用するので TemplateView の post をオーバーライドする。
    """
    template_name = 'accounts/account_delete.html'
    success_url = 'teams:home'

    def post(self, request, *args, **kwargs):
        """
        削除・削除キャンセルの処理
        """
        self.object = get_user_model().objects.get(username=self.kwargs.get('username'))
        if self.request.POST.get('confirm', '') == 'delete':
            user_profile = self.request.user.user_profile
            user_profile.is_owner = False
            user_profile.save()
            self.object.delete()
        elif self.request.POST.get('confirm', '') == 'back':
            return redirect('accounts:account_settings')
        return redirect(self.success_url)



    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(get_user_model(), username=username)

account_delete = UserDeleteView.as_view()



class UserSettingsView(LoginRequiredMixin, TemplateView):
    """
    ユーザーの設定項目を一覧表示する
    """
    template_name = 'accounts/account_settings.html'

account_settings = UserSettingsView.as_view()
