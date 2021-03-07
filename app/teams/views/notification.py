from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.models import Team, Invite, Apply, UserProfile
from teams.forms import InviteCreateForm, ApplyCreateForm
from teams.views import OnlyYouMixin



""" 招待関係 view """

class InviteNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/invite_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['invitations'] = Invite.objects.filter(
            # (from_user=self.request.user AND (is_proceeded=True OR is_prceeded=False)) OR to_user=self.request.user
            Q(from_user=self.request.user),
            Q(is_proceeded=True) |
            Q(is_proceeded=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invite_notification = InviteNotificationView.as_view()



class InviteNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
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



""" リクエスト関係 view """

class ApplyNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/apply_notification.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['applications'] = Apply.objects.filter(
            # (from_user=self.request.user AND (is_proceeded=True OR is_prceeded=False)) OR to_user=self.request.user
            # Q(from_user=self.request.user),
            # Q(is_proceeded=True) |
            # Q(is_proceeded=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        print('\n\n\n\n\n\n\n\n{}\n\n\n\n\n\n\n\n'.format(ctx))
        return ctx

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

apply_notification = ApplyNotificationView.as_view()



class ApplyNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/apply_notification_detail.html'
    model = Apply
    context_object_name = 'apply'
    success_url = 'teams:apply_reply_create'

    # 認可の処理
    def post(self, request, *args, **kwargs):
        self.object = Apply.objects.get(id=self.kwargs.get('id'))

        # すでに is_proceeded がセットされている場合処理を見送る
        # if self.object.is_proceeded is True or self.object.is_proceeded is False:
        #     pass

        # 承認ボタンなら、 True を設定する
        if self.request.POST.get('approval', '') == 'approve':
        # elif self.request.POST.get('approval', '') == 'approve':
            self.object.is_proceeded = True
            self.object.save()
            # ここでフォームがある別ページにリダイレクトする
            return redirect(self.success_url, id=self.object.id)

        # 拒否ボタンなら、 False を設定する
        elif self.request.POST.get('approval', '') == 'deny':
            self.object.is_proceeded = False
            self.object.save()

        # ここのURLのちに変更できたら変更する
        return redirect('teams:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apply'] = Apply.objects.get(id=self.kwargs.get('id'))
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    # def get_success_url(self):
    #     return reverse(self.success_url, kwargs={'username': self.request.user})

apply_notification_detail = ApplyNotificationDetailView.as_view()
