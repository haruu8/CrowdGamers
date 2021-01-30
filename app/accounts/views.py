from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserUpdateForm



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuse



# ユーザーのプロフィール
class UserDetailView(DetailView):
    template_name = 'accounts/account_detail.html'

account_detail = UserDetailView.as_view()



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
    success_url = reverse_lazy('clans:home')

account_delete = UserDeleteView.as_view()
