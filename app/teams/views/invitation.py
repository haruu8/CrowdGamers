from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from teams.models import UserProfile
from teams.forms import InvitationCreateForm
from .profile import UserProfileBaseView



class InvitationCreateView(LoginRequiredMixin, CreateView, UserProfileBaseView):
    """
    ユーザー招待を作成する
    """
    template_name = 'teams/invitation_create.html'
    form_class = InvitationCreateForm
    success_url = 'teams:account_detail'

    def form_valid(self, form):
        """
        invitation object に必要な情報を登録する

        Notes
        -----
        オーナーでなければ、プロフィールページに返す
        """
        self.object = form.save(commit=False)
        if self.request.user.user_profile.is_owner == False:
            return reverse(self.success_url, kwargs={'username': self.object.username})
        self.object.mode = 'invitation'
        self.object.from_user = self.request.user
        self.object.invitation_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        self.object.to_user = self.object.invitation_user
        self.object.save()

        result = super().form_valid(form)
        return result

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.object.invitation_user})

invitation_create = InvitationCreateView.as_view()
