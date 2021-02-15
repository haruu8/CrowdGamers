from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Clan, Invite, Apply, Question, UserProfile
from accounts.models import User
from .forms import ClanCreateForm, UserInviteCreateForm, ClanRequestCreateForm



class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuse



class HomeView(generic.TemplateView):
    template_name = 'clans/home.html'

home = HomeView.as_view()



class UserDetailGameView(DetailView):
    template_name = 'clans/accounts/account_detail_game.html'
    model = User

account_detail_game = UserDetailGameView.as_view()



class UserDetailFeatureView(DetailView):
    template_name = 'clans/accounts/account_detail_feature.html'
    model = User

account_detail_feature = UserDetailFeatureView.as_view()



class UserDetailDesiredJobTypeView(DetailView):
    template_name = 'clans/accounts/account_detail_desired_job_type.html'

account_detail_desired_job_type = UserDetailDesiredJobTypeView.as_view()



class UserInviteNoticeView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'clans/user_invite_notice.html'

    def get_context_data(self, **kwargs):

        """
            ユーザーに送った招待が承認・拒否された場合に通知
        """
        if self.request.user.is_owner == True:
            context = super().get_context_data(**kwargs)
            context['invite'] = Invite.objects.get(user=self.request.user)
            return context

user_invite_notice = UserInviteNoticeView.as_view()



class UserInviteNoticeDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'clans/user_invite_notice_detail.html'
    model = Invite

user_invite_notice_detail = UserInviteNoticeDetailView.as_view()



class UserApplyNoticeView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'clans/user_apply_notice.html'

    def get_context_data(self, **kwargs):

        """
            クランに送ったリクエストの承認可否
        """
        context = super().get_context_data(**kwargs)
        context['apply'] = Apply.objects.get(user=self.request.user)
        return context

user_apply_notice = UserApplyNoticeView.as_view()



class UserApplyNoticeDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'clans/user_apply_notice_detail.html'
    model = Apply

user_apply_notice_detail = UserApplyNoticeDetailView.as_view()



class ClanCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/clan_create.html'
    model = Clan
    form_class = ClanCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        user = form.save(commit=True)
        user.is_owner = True
        form.instance.user = self.request.user
        return super().form_valid(form)

clan_create = ClanCreateView.as_view()



class ClanListView(ListView):
    template_name = 'clans/clan_list.html'
    model = Clan

clan_list = ClanListView.as_view()



class ClanDetailView(DetailView):
    template_name = 'clans/clan_detail.html'
    model = Clan

clan_detail = ClanDetailView.as_view()



class ClanUpdateView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    template_name = 'clans/clan_update.html'
    model = Clan
    form_class = ClanCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        return redirect(self.get_success_url())

clan_update = ClanUpdateView.as_view()



class ClanDeleteView(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    template_name = 'clans/clan_delete.html'
    model = Clan
    success_url = reverse_lazy('clan:home')

clan_delete = ClanDeleteView.as_view()



""" クランリクエストに関する view """

class ClanRequestInputView(LoginRequiredMixin, generic.FormView):
    template_name = 'clans/clan_request_input.html'
    form_class = ClanRequestCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

clan_request_input = ClanRequestInputView.as_view()



class ClanRequestConfirmView(LoginRequiredMixin, FormView):
    template_name = 'clans/clan_request_confirm.html'
    form_class = ClanRequestCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'clans/clan_request_input.html', {'form': form})

clan_request_confirm = ClanRequestConfirmView.as_view()



class ClanRequestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/clan_request_input.html'
    form_class = ClanRequestCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return redirect(self.success_url)

    # エラーページに遷移するのがいいのか
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

clan_request_create = ClanRequestCreateView.as_view()



""" ユーザー招待に関する view """

class UserInviteInputView(LoginRequiredMixin, generic.FormView):
    template_name = 'clans/user_invite_input.html'
    form_class = UserInviteCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

user_invite_input = UserInviteInputView.as_view()



class UserInviteConfirmView(LoginRequiredMixin, FormView):
    template_name = 'clans/user_invite_confirm.html'
    form_class = UserInviteCreateForm

    def form_valid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'clans/user_invite_input.html', {'form': form})

user_invite_confirm = UserInviteConfirmView.as_view()



class UserInviteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clans/user_invite_input.html'
    form_class = UserInviteCreateForm
    success_url = reverse_lazy('clans:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return redirect(self.success_url)

    # エラーページに遷移するのがいいのか
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

user_invite_create = UserInviteCreateView.as_view()



class FreqentlyQuestionAskedView(generic.TemplateView):
    template_name = 'clans/support/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Question.objects.all()
        return context

faq = FreqentlyQuestionAskedView.as_view()
