from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from .forms import UserUpdateForm



user = get_user_model()



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser



class UserUpdateView(OnlyYouMixin, LoginRequiredMixin, UpdateView):
    template_name = 'accounts/account_update.html'
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:account_detail')

    def form_valid(self, form):
        return redirect(self.get_success_url())

account_update = UserUpdateView.as_view()



class UserDeleteView(OnlyYouMixin, LoginRequiredMixin, DeleteView):
    template_name = 'accounts/account_delete.html'
    model = User
    success_url = reverse_lazy('teams:home')

account_delete = UserDeleteView.as_view()



class UserListView(ListView):
    template_name = 'accounts/account_list.html'
    model = User

account_list = UserListView.as_view()



class UserSettingsView(OnlyYouMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/account_settings.html'

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

account_settings = UserSettingsView.as_view()
