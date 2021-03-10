from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.models import Team, UserProfile, Notification
from teams.forms import InvitationCreateForm, ApplicationCreateForm
from teams.views import OnlyYouMixin


class InvitationNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    """
    招待を一覧表示する
    """
    template_name = 'teams/notification/invite_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['invitations'] = Notification.objects.filter(
            Q(from_user=self.request.user),
            Q(is_proceeded__isnull=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invite_notification = InvitationNotificationView.as_view()



class InvitationNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    招待の詳細を表示する
    """
    template_name = 'teams/notification/invite_notification_detail.html'
    model = Notification
    context_object_name = 'invite'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invite'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invite_notification_detail = InvitationNotificationDetailView.as_view()



class ApplicationNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    """
    チームに対するリクエスト・メンバー追加のリクエストの両方を表示する

    Notes
    -----
    モデルは違うが、日付順に並べるため ctx を結合している
    """
    template_name = 'teams/notification/apply_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx1 = super().get_context_data(**kwargs)
        ctx['applications'] = Notification.objects.filter(
            Q(from_user=self.request.user),
            Q(is_proceeded__isnull=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')

        ctx1['applications'] = Notification.objects.filter(
            Q(from_user=self.request.user),
            Q(is_proceeded__isnull=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        print('\n\n\n\n\n\n\n{}\n\n\n\n\n\n\n'.format(ctx))
        print('\n\n\n\n\n\n\n{}\n\n\n\n\n\n\n'.format(ctx1))
        return ctx

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

apply_notification = ApplicationNotificationView.as_view()



class MemberApprovalNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    チームのメンバー追加の詳細を表示する
    """
    template_name = 'teams/notification/member_approval_notification_detail.html'
    model = Notification
    success_url = 'teams:notification'

    def post(self, request, *args, **kwargs):
        """
        チームのメンバー登録申請の認可

        Notes
        -----
        self.object は memberApproval オブジェクトを管理
        チーム登録は new_* と命名している
        """
        self.object = Notification.objects.get(id=self.kwargs.get('id'))
        if self.object.is_proceeded is True or self.object.is_proceeded is False:
            pass
        elif self.request.POST.get('approval', '') == 'approve':
            self.object.is_proceeded = True
            new_team = self.object.to_user.user_profile.team
            new_member_profile = self.object.from_user.user_profile
            new_member_profile.team = new_team
            new_member_profile.save()
        elif self.request.POST.get('approval', '') == 'deny':
            self.object.is_proceeded = False
        self.object.save()
        return redirect('teams:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_approval'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

member_approval_notification_detail = MemberApprovalNotificationDetailView.as_view()



class ApplicationNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    リクエストの詳細を表示する
    """
    template_name = 'teams/notification/apply_notification_detail.html'
    model = Notification
    success_url = 'teams:apply_reply_create'

    def post(self, request, *args, **kwargs):
        """
        申請の認可の処理

        Notes
        -----
        承認なら ApplicationReplyCreateView での処理
        拒否なら apply object の is_proceeded に False をセットする
        """
        self.object = Notification.objects.get(id=self.kwargs.get('id'))
        if self.object.is_proceeded is True or self.object.is_proceeded is False:
            pass
        elif self.request.POST.get('approval', '') == 'approve':
            return redirect(self.success_url, username=self.request.user.username, id=self.object.id)
        elif self.request.POST.get('approval', '') == 'deny':
            self.object.is_proceeded = False
            self.object.save()
        return redirect('teams:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apply'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

apply_notification_detail = ApplicationNotificationDetailView.as_view()
