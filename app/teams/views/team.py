from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from teams.models import Team, UserProfile
from teams.forms import TeamCreateForm
from .utils import OnlyYouMixin, OnlyOwnerMixin, GetProfileView
from accounts.models import User



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        profile = self.request.user.user_profile

        # is_owner True, profile.team があれば作成できない
        if profile.is_owner is True or profile.team:
            form.add_error(None, 'チームは1つまでしか所属できません。')
            return render(self.request, self.template_name, {'form': form})

        result = super().form_valid(form)
        profile.is_owner = True
        profile.team = self.object
        profile.save()
        return result

    def get_success_url(self):
        return reverse('teams:team_detail_game', kwargs={'teamname': self.object.teamname})

team_create = TeamCreateView.as_view()



class TeamListView(ListView):
    template_name = 'teams/team_list.html'
    model = Team

team_list = TeamListView.as_view()



class TeamUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'teams/team_update.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        return redirect(self.get_success_url())

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_update = TeamUpdateView.as_view()



class TeamDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    template_name = 'teams/team_delete.html'
    model = Team
    success_url = reverse_lazy('team:home')

team_delete = TeamDeleteView.as_view()



class TeamDetailBaseView(DetailView):
    template_name = 'teams/team_detail.html'
    model = Team
    form_class = TeamCreateForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, teamname=self.kwargs.get("teamname"))
        owner_profile = team.belonging_user_profiles.filter(is_owner=True)[0]
        context['owner_profile_user_username'] = owner_profile.user.username
        context['owner_profile_icon_url'] = owner_profile.icon.url
        context['owner_profile_name'] = owner_profile.name
        return context

team_detail_member = TeamDetailMemberView.as_view()



class TeamDetailFeatureView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_feature.html'
    model = Team

team_detail_feature = TeamDetailFeatureView.as_view()



class TeamDetailDesiredConditionView(TeamDetailBaseView):
    template_name = 'teams/team_profile/team_detail_desired_condition.html'
    model = Team

team_detail_desired_condition = TeamDetailDesiredConditionView.as_view()
