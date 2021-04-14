from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from teams.models import Team, UserProfile, Notification
from teams.forms import InvitationCreateForm, ApplicationCreateForm
from teams.views import OnlyYouMixin



class NotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    """
    ログインユーザーの通知を一覧表示する。
    """
    template_name = 'teams/notification/notification.html'

    def get_context_data(self, **kwargs):
        """
        ログインユーザーの通知のデータを取得する関数。

        Returns
        -------
        dict
            Notification オブジェクト入り ctx。
        """
        ctx = super().get_context_data(**kwargs)
        ctx['notifications'] = Notification.objects.filter(
            Q(from_user=self.request.user, is_proceeded__isnull=False) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')
        return ctx

notification = NotificationView.as_view()



class NotificationDetailBaseView(OnlyYouMixin, DetailView):
    """
    通知詳細画面の共通部分をまとめた view 。
    application, invitation, member_approval に対応している。
    """
    template_name = 'teams/notification/official_detail.html'
    model = Notification
    context_object_name = 'object'

    def get(self, request, *args, **kwargs):
        """
        詳細画面に表示するために必要な情報を取得する。
        """
        notification_obj = Notification.objects.get(id=self.kwargs.get('id'))
        if self.request.user == notification_obj.from_user and notification_obj.is_proceeded is None:
            return redirect('teams:home')
        if self.request.user == notification_obj.from_user:
            notification_obj.sender_has_read = True
        elif self.request.user == notification_obj.to_user:
            notification_obj.reciever_has_read = True
        notification_obj.save()
        ctx = {
            'object': notification_obj
        }
        return render(self.request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        """
        認可をオブジェクトに登録する関数。
        ボタンの属性から認可を判断する。
        application だけ、別リンクに飛ばしたいので、処理を変えている箇所がある。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            引数で指定しているルーティングに redirect。
        """
        self.object = Notification.objects.get(id=self.kwargs.get('id'))
        if self.object.from_user == self.request.user:
            return redirect('teams:home')
        if self.object.is_proceeded is True or self.object.is_proceeded is False:
            pass
        elif self.object.mode == 'application':
            if self.request.POST.get('approval', '') == 'approve':
                return redirect(self.success_url, username=self.request.user.username, id=self.object.id)
            elif self.request.POST.get('approval', '') == 'deny':
                self.object.is_proceeded = False
        elif self.request.POST.get('approval', '') == 'approve':
            self.object.is_proceeded = True
        elif self.request.POST.get('approval', '') == 'deny':
            self.object.is_proceeded = False
        self.object.save()
        return redirect('teams:home')

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))




class InvitationNotificationDetailView(NotificationDetailBaseView):
    template_name = 'teams/notification/invitation_detail.html'

invitation_detail = InvitationNotificationDetailView.as_view()



class ApplicationNotificationDetailView(NotificationDetailBaseView):
    success_url = 'teams:application_reply_create'
    template_name = 'teams/notification/application_detail.html'

application_detail = ApplicationNotificationDetailView.as_view()



class MemberApprovalNotificationDetailView(NotificationDetailBaseView):
    template_name = 'teams/notification/member_approval_detail.html'

member_approval_detail = MemberApprovalNotificationDetailView.as_view()



class OfficialNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    公式からのお知らせの詳細を表示する。
    """
    template_name = 'teams/notification/official_detail.html'
    model = Notification

    def get_context_data(self, **kwargs):
        """
        公式からのお知らせの詳細画面に表示するために必要な情報を取得する関数。
        既読をつける処理も入っている。

        Returns
        -------
        dict
            チームリクエストオブジェクト入り ctx。
        """
        ctx = super().get_context_data(**kwargs)
        notification_obj = Notification.objects.get(id=self.kwargs.get('id'))
        if self.request.user == notification_obj.from_user:
            notification_obj.sender_has_read = True
        elif self.request.user == notification_obj.to_user:
            notification_obj.reciever_has_read = True
        notification_obj.save()
        ctx['official_notification'] = notification_obj
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

official_detail = OfficialNotificationDetailView.as_view()
