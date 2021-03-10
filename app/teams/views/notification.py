from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.models import Team, UserProfile, Notification
from teams.forms import InvitationCreateForm, ApplicationCreateForm
from teams.views import OnlyYouMixin



class NotificationView(LoginRequiredMixin, OnlyYouMixin,TemplateView):
    """
    通知を一覧表示する

    TODO
    -----
    全ての通知を取得する処理を書く
    """
    template_name = 'teams/notification/notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['notifications'] = Notification.objects.filter(
        #     Q(from_user=self.request.user),
        #     Q(is_proceeded__isnull=False) |
        #     Q(to_user=self.request.user)
        # ).order_by('-created_at')
        ctx['notifications'] = Notification.objects.filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

notification = NotificationView.as_view()



class InvitationNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    招待の詳細を表示する
    """
    template_name = 'teams/notification/invitation_detail.html'
    model = Notification
    context_object_name = 'invitation'

    def post(self, request, *args, **kwargs):
        """
        招待の承認・拒否の処理
        """
        self.object = Notification.objects.get(id=self.kwargs.get('id'))
        if self.object.is_proceeded is True or self.object.is_proceeded is False:
            pass
        elif self.request.POST.get('approval', '') == 'approve':
            self.object.is_proceeded = True
        elif self.request.POST.get('approval', '') == 'deny':
            self.object.is_proceeded = False
        self.object.save()
        return redirect('teams:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invitation'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invitation_detail = InvitationNotificationDetailView.as_view()



class MemberApprovalNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    チームのメンバー追加の詳細を表示する
    """
    template_name = 'teams/notification/member_approval_detail.html'
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

member_approval_detail = MemberApprovalNotificationDetailView.as_view()



class ApplicationNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    リクエストの詳細を表示する
    """
    template_name = 'teams/notification/application_detail.html'
    model = Notification
    success_url = 'teams:application_reply_create'

    def post(self, request, *args, **kwargs):
        """
        申請の認可の処理

        Notes
        -----
        承認なら ApplicationReplyCreateView での処理
        拒否なら application object の is_proceeded に False をセットする
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
        context['application'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

application_detail = ApplicationNotificationDetailView.as_view()



class OfficialNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    公式からのお知らせの詳細を表示する
    """
    template_name = 'teams/notification/official_detail.html'
    model = Notification

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['official_notification'] = Notification.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

official_detail = OfficialNotificationDetailView.as_view()
