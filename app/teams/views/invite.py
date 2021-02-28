from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from teams.models import Invite
from teams.forms import UserInviteCreateForm



""" ユーザー招待に関する view """

class UserInviteInputView(LoginRequiredMixin, generic.FormView):
    template_name = 'teams/invite/user_invite_input.html'
    form_class = UserInviteCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

user_invite_input = UserInviteInputView.as_view()



class UserInviteConfirmView(LoginRequiredMixin, FormView):
    template_name = 'teams/invite/user_invite_confirm.html'
    form_class = UserInviteCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'teams/user_invite_input.html', {'form': form})

user_invite_confirm = UserInviteConfirmView.as_view()



class UserInviteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/invite/user_invite_input.html'
    form_class = UserInviteCreateForm
    success_url = reverse_lazy('teams:home')

    # from と to を設定
    # オーナーしか送信できないようにする
    def form_valid(self, form):
        form.instance.user = self.request.user

        """
            * from user に自分を登録 (owner前提)
            self.object.from_user = self.request.user

            *** to_user にユーザーを保存 ***
              * 送ろうとしているユーザーのオブジェクトを取得する
              * object の to_user に 招待を送るユーザーを登録

            invitation_user = User.objects.get(username=username)
            self.object.to_user = invitation_user
        """

        result = super().form_valid(form)
        return result

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

    def get_success_url(self):
        return reverse('teams:account_detail_game', kwargs={'username': self.object.username})

user_invite_create = UserInviteCreateView.as_view()
