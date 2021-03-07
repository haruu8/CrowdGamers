from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Apply, Team
from django.contrib.auth import get_user_model
from teams.forms import ApplyCreateForm, ApplyUpdateForm
from .team import TeamDetailBaseView



""" クランリクエストに関する view """

class ApplyCreateView(LoginRequiredMixin, CreateView, TeamDetailBaseView):
    template_name = 'teams/apply_create.html'
    form_class = ApplyCreateForm
    success_url = 'teams:team_detail'

    # from と to を設定
    def form_valid(self, form):
        self.object = form.save(commit=False)

        # from_user に request user を保存
        self.object.from_user = self.request.user

        # to_user にチームのオーナーを保存
        self.object.team = Team.objects.get(teamname=self.kwargs.get('teamname'))
        member = self.object.team.belonging_user_profiles.all()
        owner_profile = member.filter(is_owner=True)[0]
        self.object.to_user = owner_profile.user
        self.object.save()
        result = super().form_valid(form)
        return result

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

apply_create = ApplyCreateView.as_view()



""" きた申請を承認した場合に必要な招待URL """

class ApplyReplyCreateView(UpdateView):
    template_name = 'teams/notification/apply_reply_create.html'
    form_class = ApplyUpdateForm
    success_url = 'teams:apply_notification'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_proceeded = True
        self.object.save()
        result = super().form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apply'] = Apply.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username})

apply_reply_create = ApplyReplyCreateView.as_view()
