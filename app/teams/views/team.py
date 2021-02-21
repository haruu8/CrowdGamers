from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from accounts.models import User
from teams.models import Team
from teams.forms import TeamCreateForm
from teams.views import OnlyYouMixin



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    # プロフィールの is_owner を変更するように変更
    def form_valid(self, form):
        user = form.save(commit=True)
        user.is_owner = True
        form.instance.user = self.request.user
        return super().form_valid(form)

team_create = TeamCreateView.as_view()



class TeamListView(ListView):
    template_name = 'teams/team_list.html'
    model = Team

team_list = TeamListView.as_view()



class TeamDetailView(DetailView):
    template_name = 'teams/team_detail.html'
    model = Team

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_detail = TeamDetailView.as_view()



class TeamUpdateView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    template_name = 'teams/team_update.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        return redirect(self.get_success_url())

team_update = TeamUpdateView.as_view()



class TeamDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    template_name = 'teams/team_delete.html'
    model = Team
    success_url = reverse_lazy('team:home')

team_delete = TeamDeleteView.as_view()



class TeamDetailView(DetailView):
    template_name = 'teams/team_detail.html'
    model = Team

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_detail = TeamDetailView.as_view()
