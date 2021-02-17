from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Team, Invite, Apply, Question, UserProfile
from accounts.models import User
from .forms import TeamCreateForm, UserInviteCreateForm, TeamApplyCreateForm



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuse



class HomeView(generic.TemplateView):
    template_name = 'teams/home.html'

home = HomeView.as_view()



""" UserProfileに関するview """

class UserDetailGameView(DetailView):
    template_name = 'teams/accounts/account_detail_game.html'
    model = UserProfile

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

account_detail_game = UserDetailGameView.as_view()



class UserDetailFeatureView(DetailView):
    template_name = 'teams/accounts/account_detail_feature.html'
    model = UserProfile

    def get_object(self):
        username= self.kwargs.get("username")
        return get_object_or_404(User, username=username)

account_detail_feature = UserDetailFeatureView.as_view()



class UserDetailDesiredJobTypeView(DetailView):
    template_name = 'teams/accounts/account_detail_desired_job_type.html'
    model = UserProfile

    def get_object(self):
        username= self.kwargs.get("username")
        return get_object_or_404(User, username=username)

account_detail_desired_job_type = UserDetailDesiredJobTypeView.as_view()



class UserInviteNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/user_invite_notification.html'

    def get_context_data(self, **kwargs):

        """
            ユーザーに送った招待が承認・拒否された場合に通知
        """
        if self.request.user.is_owner == True:
            context = super().get_context_data(**kwargs)
            context['invite'] = Invite.objects.get(user=self.request.user)
            return context

user_invite_notification = UserInviteNotificationView.as_view()



class UserInviteNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/user_invite_notification_detail.html'
    model = Invite

user_invite_notification_detail = UserInviteNotificationDetailView.as_view()



class UserApplyNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/user_apply_notification.html'

    def get_context_data(self, **kwargs):

        """
            クランに送ったリクエストの承認可否
        """
        context = super().get_context_data(**kwargs)
        context['apply'] = Apply.objects.get(user=self.request.user)
        return context

user_apply_notification = UserApplyNotificationView.as_view()



class UserApplyNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/user_apply_notification_detail.html'
    model = Apply

user_apply_notification_detail = UserApplyNotificationDetailView.as_view()



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

team_apply_create = TeamApplyCreateView.as_view()



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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, '400.html', {'form': form})

user_invite_create = UserInviteCreateView.as_view()



class FreqentlyQuestionAskedView(generic.TemplateView):
    template_name = 'teams/support/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Question.objects.all()
        return context

faq = FreqentlyQuestionAskedView.as_view()
