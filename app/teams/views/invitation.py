from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from teams.models import UserProfile
from teams.forms import InvitationCreateForm
from .profile import UserProfileBaseView



""" ユーザー招待に関する view """

class InvitationCreateView(LoginRequiredMixin, CreateView, UserProfileBaseView):
    template_name = 'teams/invitation_create.html'
    form_class = InvitationCreateForm
    success_url = 'teams:account_detail'

    # from と to を設定
    def form_valid(self, form):
        self.object = form.save(commit=False)

        # オーナーでなければ、プロフィールページに返す
        if self.request.user.user_profile.is_owner == False:
            return reverse(self.success_url, kwargs={'username': self.object.username})

        # from_user を登録
        self.object.from_user = self.request.user

        # to_user を登録
        self.object.invitation_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        self.object.to_user = self.object.invitation_user
        self.object.save()

        result = super().form_valid(form)
        return result

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.object.invitation_user})

invitation_create = InvitationCreateView.as_view()