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
    チームリクエストを作成する
    """
    template_name = 'teams/application_create.html'
    form_class = ApplicationCreateForm
    success_url = 'teams:team_detail'

    def form_valid(self, form):
        """
        application object に必要な情報を登録する

        Notes
        -----
        mode に application を保存
        from_user に request.user を保存
        to_user にチームのオーナーを保存
        """
        self.object = form.save(commit=False)
        self.object.mode = 'application'
        self.object.from_user = self.request.user

        self.object.team = Team.objects.get(teamname=self.kwargs.get('teamname'))
        member = self.object.team.belonging_user_profiles.all()
        owner_profile = member.filter(is_owner=True)[0]
        self.object.to_user = owner_profile.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

application_create = ApplicationCreateView.as_view()



class ApplicationReplyCreateView(OnlyYouMixin, UpdateView):
    """
    リクエストの承認とその返答に必要なURLを設定するURL

    TODO
    -----
    直接URLを入力するとアクセスすることができるので、修正する
    """
    template_name = 'teams/notification/application_reply_create.html'
    form_class = ApplicationUpdateForm
    success_url = 'teams:notification'

    def form_valid(self, form):
        """
        認可を True にするのとURLをDBに登録するフォーム
        """
        self.object = Notification.objects.get(id=self.kwargs.get('id'))
        self.object.is_proceeded = True
        self.object.invite_url = form.cleaned_data['invite_url']
        self.object.save()
        result = super().form_valid(form)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username})

application_reply_create = ApplicationReplyCreateView.as_view()
