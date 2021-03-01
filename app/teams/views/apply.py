from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Apply, Team
from teams.forms import TeamApplyCreateForm
from .team import TeamDetailBaseView



""" クランリクエストに関する view """

class TeamApplyInputView(LoginRequiredMixin, FormView, TeamDetailBaseView):
    template_name = 'teams/apply/team_apply_input.html'
    form_class = TeamApplyCreateForm
    model = Team

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

apply_input = TeamApplyInputView.as_view()



class TeamApplyConfirmView(LoginRequiredMixin, FormView, TeamDetailBaseView):
    template_name = 'teams/apply/team_apply_confirm.html'
    form_class = TeamApplyCreateForm
    model = Team

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'teams/apply/team_apply_input.html', {'form': form})

apply_confirm = TeamApplyConfirmView.as_view()



class TeamApplyCreateView(LoginRequiredMixin, CreateView, TeamDetailBaseView):
    template_name = 'teams/apply/team_apply_input.html'
    form_class = TeamApplyCreateForm
    success_url = reverse_lazy('teams:team_detail_game')

    # from と to を設定
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # form.instance.user = self.request.user


        # from_user に request user を保存
        self.object.from_user = self.request.user

        self.object.team = get_object_or_404(Team, teamname=self.kwargs.get('teamname'))

        # to_user にチームのオーナーを保存

        # todo: ユーザーネーム取得の処理を書く
        team = Team.objects.get(teamname=self.object.team.teamname)
        member = team.belonging_user_profiles
        owner_profile = member.objects.filter(is_owner=True)[0]
        owner = owner_profile.user
        self.object.to_user = owner

        self.object.save()
        result = super().form_valid(form)
        return result

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.teamname})

apply_create = TeamApplyCreateView.as_view()
