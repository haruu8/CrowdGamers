from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Apply, Team
from teams.forms import TeamApplyCreateForm



""" クランリクエストに関する view """

class TeamApplyInputView(LoginRequiredMixin, FormView):
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

        """
            * from_user に request user を保存
            self.object.from_user = self.request.user

            *** to_user にチームのオーナーを保存 ***
              * 送ろうとしているチームのオブジェクトを取得する
              * チームのメンバーを一覧取得し、そのあとに owner True でフィルター
              * object の to_user に is_owner のユーザーを登録する

            team = Team.objects.get(teamname=???)
        """


        result = super().form_valid(form)
        return result

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

    def get_success_url(self):
        return reverse('teams:team_detail_game', kwargs={'teamname': self.object.teamname})

    def get_object(self):
        return get_object_or_404(Team, teamname=self.kwargs.get('teamname'))

team_apply_create = TeamApplyCreateView.as_view()
