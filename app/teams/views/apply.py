from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Apply
from teams.forms import TeamApplyCreateForm



""" クランリクエストに関する view """

class TeamApplyInputView(LoginRequiredMixin, generic.FormView):
    template_name = 'teams/apply/team_apply_input.html'
    form_class = TeamApplyCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

team_apply_input = TeamApplyInputView.as_view()



class TeamApplyConfirmView(LoginRequiredMixin, FormView):
    template_name = 'teams/apply/team_apply_confirm.html'
    form_class = TeamApplyCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'teams/apply/team_apply_input.html', {'form': form})

team_apply_confirm = TeamApplyConfirmView.as_view()



class TeamApplyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/apply/team_apply_input.html'
    form_class = TeamApplyCreateForm
    success_url = reverse_lazy('teams:home')

    # from と to を設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        result = super().form_valid(form)
        return result

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

    def get_success_url(self):
        return reverse('teams:team_detail_game', kwargs={'teamname': self.object.teamname})

team_apply_create = TeamApplyCreateView.as_view()

