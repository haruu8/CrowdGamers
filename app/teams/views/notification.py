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



class InvitationNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    招待の詳細を表示する。
    """
    template_name = 'teams/notification/invitation_detail.html'
    model = Notification
    context_object_name = 'invitation'

    def post(self, request, *args, **kwargs):
        """
        招待の認可をオブジェクトに登録する関数。
        ボタンの属性から認可を判断する。

        Returns
        -------
        redirect('teams:home') : Callable
            引数の url にリダイレクト。
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
        """
        招待詳細画面に表示するために必要な情報を取得する関数。
        既読もつける。

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
        ctx['invitation'] = notification_obj
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

invitation_detail = InvitationNotificationDetailView.as_view()



class MemberApprovalNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    チームのメンバー追加の詳細を表示する。
    """
    template_name = 'teams/notification/member_approval_detail.html'
    model = Notification
    success_url = 'teams:notification'

    def post(self, request, *args, **kwargs):
        """
        チームのメンバー登録申請の認可に関するデータを登録する関数。
        ボタンの属性から認可を判断する。

        Returns
        -------
        redirect('teams:home') : Callable
            引数の url にリダイレクト。
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
        """
        メンバー追加申請の詳細画面に表示するために必要な情報を取得する関数。
        既読もつける。

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
        ctx['member_approval'] = notification_obj
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        """
        button が押されたタイミングでリダイレクトする URL を取得する関数。

        Parameters
        ----------
        self.request.user.username : str
            request.user の username。
        self.object.id : str
            同クラスの post 関数で取得した member_approval object の id。
        """
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

member_approval_detail = MemberApprovalNotificationDetailView.as_view()



class ApplicationNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    リクエストの詳細を表示する。
    """
    template_name = 'teams/notification/application_detail.html'
    model = Notification
    success_url = 'teams:application_reply_create'

    def post(self, request, *args, **kwargs):
        """
        詳細画面に表示される認可のデータ保存処理を行う関数。
        ボタンの属性から認可を判断する。
        is_proceeded が True なら 別 view での処理、 False なら application object の is_proceeded に False を登録。

        Returns
        -------
        redirect('teams:home') : Callable
            引数の url にリダイレクト。
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
        """
        チームリクエスト詳細画面に表示するために必要な情報を取得する関数。
        既読もつける。

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
        ctx['application'] = notification_obj
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

    def get_success_url(self):
        """
        button が押されたタイミングでリダイレクトする URL を取得する関数。

        Parameters
        ----------
        self.request.user.username : str
            request.user の username。
        self.object.id : str
            同クラスの post 関数で取得した application object の id。
        """
        return reverse(self.success_url, kwargs={'username': self.request.user.username, 'id': self.object.id})

application_detail = ApplicationNotificationDetailView.as_view()



class OfficialNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    """
    公式からのお知らせの詳細を表示する。
    """
    template_name = 'teams/notification/official_detail.html'
    model = Notification

    def get_context_data(self, **kwargs):
        """
        公式からのお知らせの詳細画面に表示するために必要な情報を取得する関数。
        既読もつける。

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
