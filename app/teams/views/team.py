from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from teams.models import Team, UserProfile
from teams.forms import TeamCreateForm
from .utils import OnlyYouMixin, GetProfileView
from accounts.models import User



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    # プロフィールの is_owner を変更するように変更
    # userprofile の team field も結びつける
    def form_valid(self, form):
        team = form.save(commit=False)
        is_owner = self.request.user.user_profile.is_owner
        if is_owner is not True:
            form.instance.user = self.request.user
            user = User.objects.get(username=self.request.user)

            # related name で参照
            profile = user.user_profile
            profile.is_owner = True
            team.save()
            profile.save()
            print('\n\n\n\n\n処理完了\n\n\n\n\n')
            return super().form_valid(form)
        else:
            # エラ〜メッセージを追加する
            return redirect('teams:home')

team_create = TeamCreateView.as_view()



class TeamListView(ListView, GetProfileView):
    template_name = 'teams/team_list.html'
    model = Team

team_list = TeamListView.as_view()



class TeamDetailView(DetailView, GetProfileView):
    template_name = 'teams/team_detail.html'
    model = Team

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_detail = TeamDetailView.as_view()



class TeamUpdateView(LoginRequiredMixin, OnlyYouMixin, UpdateView, GetProfileView):
    template_name = 'teams/team_update.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        return redirect(self.get_success_url())

team_update = TeamUpdateView.as_view()



class TeamDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView, GetProfileView):
    template_name = 'teams/team_delete.html'
    model = Team
    success_url = reverse_lazy('team:home')

team_delete = TeamDeleteView.as_view()



class TeamDetailBaseView(DetailView, GetProfileView):
    template_name = 'teams/team_detail.html'
    model = Team
    form_class = TeamCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['owner_profile'] = UserProfile.objects.filter(team=team, is_owner=True)
        return context

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)



class TeamDetailGameView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_game.html'
    model = Team

team_detail_game = TeamDetailGameView.as_view()



class TeamDetailMemberView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_member.html'
    model = Team

team_detail_member = TeamDetailMemberView.as_view()



class TeamDetailFeatureView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_feature.html'
    model = Team

team_detail_feature = TeamDetailFeatureView.as_view()



class TeamDetailDesiredConditionView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_desired_condition.html'
    model = Team

team_detail_desired_condition = TeamDetailDesiredConditionView.as_view()
