from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .access import OnlyYouMixin
from teams.models import Team, Notification
from teams.forms import ApplicationCreateForm, ApplicationUpdateForm
from .team import TeamDetailBaseView



class ApplicationCreateView(LoginRequiredMixin, CreateView, TeamDetailBaseView):
    """
    チームリクエストを作成する。
    """
    template_name = 'teams/application_create.html'
    form_class = ApplicationCreateForm
    success_url = 'teams:team_detail'
    team_model = Team

    def form_valid_for_create_view(self, form):
        return super().form_valid(form)

    def form_valid(self, form):
        """
        application object に必要な情報を登録する。
        同じチームに所属している場合、無効になる。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            success_url に redirect。
        """
        self.object = form.save(commit=False)
        self.object.team = self.team_model.objects.get(teamname=self.kwargs.get('teamname'))
        self.user_team = self.request.user.user_profile.team
        if self.object.team == self.user_team or self.object.team.disclosed is False:
            return redirect(self.success_url, teamname=self.kwargs.get('teamname'))

        self.object.mode = 'application'
        self.object.from_user = self.request.user

        member = self.object.team.belonging_user_profiles.all()
        owner_profile = member.filter(is_owner=True)[0]
        self.object.to_user = owner_profile.user
        self.object.save()
        return self.form_valid_for_create_view(form)

    def get_success_url(self):
        """
        super().form_valid(form) が実行された後にリダイレクトする URL を取得する関数。

        See Also
        --------
        self.object.team.teamname : str
            form_valid 関数で取得したリクエストを送ろうとしている Team の teamname。
        """
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

application_create = ApplicationCreateView.as_view()



class ApplicationReplyCreateView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    """
    リクエストの承認とその返答に必要なURLを入力するための view。
    """
    template_name = 'teams/notification/application_reply_create.html'
    form_class = ApplicationUpdateForm
    success_url = 'teams:notification'

    def form_valid_for_create_view(self, form):
        return super().form_valid(form)

    def form_valid(self, form):
        """
        チームリクエストオブジェクトを True にするのとURLをオブジェクトに登録する関数。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            get_success_url 関数で指定した url に redirect。
        """
        self.object = Notification.objects.get(id=self.kwargs.get('id'))
        if self.object.from_user == self.request.user or self.object.is_proceeded is False:
            return redirect('teams:home')
        self.object.is_proceeded = True
        self.object.invitation_url = form.cleaned_data['invitation_url']
        self.object.save()
        return self.form_valid_for_create_view(form)

    def get_context_data(self, **kwargs):
        """
        チームリクエストオブジェクトの編集に必要なオブジェクトを取得する関数。

        Returns
        -------
        dict
            チームリクエストオブジェクト入り ctx。
        """
        ctx = super().get_context_data(**kwargs)
        ctx['object'] = Notification.objects.get(id=self.kwargs.get('id'))
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        """
        super().form_valid(form) が実行された後にリダイレクトする URL を取得する関数。

        See Also
        --------
        self.request.user.username : str
            request.user の username。
        """
        return reverse(self.success_url, kwargs={'username': self.request.user.username})

application_reply_create = ApplicationReplyCreateView.as_view()
