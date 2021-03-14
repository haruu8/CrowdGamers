from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from teams.models import UserProfile
from teams.forms import InvitationCreateForm
from .profile import UserProfileBaseView



class InvitationCreateView(LoginRequiredMixin, CreateView, UserProfileBaseView):
    """
    ユーザー招待を作成する。
    """
    template_name = 'teams/invitation_create.html'
    form_class = InvitationCreateForm
    success_url = 'teams:account_detail'

    def form_valid(self, form):
        """
        invitation object に必要な情報を登録する。
        オーナーでない場合、無効になる。

        Returns
        -------
        redirect(self.success_url, teamname=self.kwargs.get('teamname')) : Callable
            自身がオーナーでなければ success_url にリダイレクト。
        super().form_valid(form) : Callable
            親クラス(CreateView)の form_valid 関数。
        """
        self.object = form.save(commit=False)
        if self.request.user.user_profile.is_owner == False:
            return redirect(self.success_url, teamname=self.kwargs.get('teamname'))
        self.object.mode = 'invitation'
        self.object.from_user = self.request.user
        self.object.invitation_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        self.object.to_user = self.object.invitation_user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        super().form_valid(form) が実行された後にリダイレクトする URL を取得する関数。

        Parameters
        ----------
        self.object.invitation_user : str
            招待を送ったユーザーの username
        """
        return reverse(self.success_url, kwargs={'username': self.object.invitation_user.username})

invitation_create = InvitationCreateView.as_view()
