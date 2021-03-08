from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.models import Team, Invite, Apply, UserProfile
from teams.forms import InviteCreateForm, ApplyCreateForm
from teams.views import OnlyYouMixin



class InviteNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    """
    招待を一覧表示する
    """
    template_name = 'teams/notification/invite_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['invitations'] = Invite.objects.filter(
            Q(from_user=self.request.user),
            Q(is_proceeded__isnull=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invite_notification = InviteNotificationView.as_view()



class InviteNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    招待の詳細を表示する
    """
    template_name = 'teams/notification/invite_notification_detail.html'
    model = Invite
    context_object_name = 'invite'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invite'] = Invite.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invite_notification_detail = InviteNotificationDetailView.as_view()



class ApplyNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    """
    リクエストを一覧表示する
    """
    template_name = 'teams/notification/apply_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['applications'] = Apply.objects.filter(
            Q(from_user=self.request.user),
            Q(is_proceeded__isnull=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

apply_notification = ApplyNotificationView.as_view()



class ApplyNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    リクエストの詳細を表示する
    """
    template_name = 'teams/notification/apply_notification_detail.html'
    model = Apply
    context_object_name = 'apply'
    success_url = 'teams:apply_reply_create'

    def post(self, request, *args, **kwargs):
        """
        申請の認可の処理

        Notes
        -----
        承認なら ApplyReplyCreateView での処理
        拒否なら apply object の is_proceeded に False をセットする
        """
        self.object = Apply.objects.get(id=self.kwargs.get('id'))
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
        context['apply'] = Apply.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

apply_notification_detail = ApplyNotificationDetailView.as_view()
