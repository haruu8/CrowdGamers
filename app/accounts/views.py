from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, DeleteView, ListView
from django.contrib.auth import get_user_model, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.views import OnlyYouMixin, AnonymousRequiredMixin



class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    """
    ログインする
    """
    template_name = 'accounts/login.html'



class UserDeleteView(OnlyYouMixin, LoginRequiredMixin, DeleteView):
    """
    ユーザーを削除する
    """
    template_name = 'accounts/account_delete.html'
    model = get_user_model()
    success_url = reverse_lazy('teams:home')

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
