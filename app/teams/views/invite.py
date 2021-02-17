from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Invite
from teams.forms import UserInviteCreateForm



""" ユーザー招待に関する view """

class UserInviteInputView(LoginRequiredMixin, generic.FormView):
    template_name = 'teams/invite/user_invite_input.html'
    form_class = UserInviteCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

user_invite_input = UserInviteInputView.as_view()



class UserInviteConfirmView(LoginRequiredMixin, FormView):
    template_name = 'teams/invite/user_invite_confirm.html'
    form_class = UserInviteCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'teams/user_invite_input.html', {'form': form})

user_invite_confirm = UserInviteConfirmView.as_view()



class UserInviteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/invite/user_invite_input.html'
    form_class = UserInviteCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

user_invite_create = UserInviteCreateView.as_view()
