from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from .forms import UserUpdateForm
from teams.views import OnlyYouMixin, AnonymousRequiredMixin
from django.contrib.auth import views as auth_views



class LoginView(auth_views.LoginView, AnonymousRequiredMixin):
    template_name = 'accounts/login.html'



class UserDeleteView(OnlyYouMixin, LoginRequiredMixin, DeleteView):
    template_name = 'accounts/account_delete.html'
    model = User
    success_url = reverse_lazy('teams:home')

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

account_delete = UserDeleteView.as_view()



class UserListView(ListView):
    template_name = 'accounts/account_list.html'
    model = User

account_list = UserListView.as_view()



class UserSettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/account_settings.html'

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

account_settings = UserSettingsView.as_view()
