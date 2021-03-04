from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Apply, Team
from teams.forms import ApplyCreateForm
from .team import TeamDetailBaseView



""" クランリクエストに関する view """

class ApplyCreateView(LoginRequiredMixin, CreateView, TeamDetailBaseView):
    template_name = 'teams/apply/apply_create.html'
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

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

apply_create = ApplyCreateView.as_view()
