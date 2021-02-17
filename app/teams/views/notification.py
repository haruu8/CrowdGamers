from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Team, Invite, Apply
from accounts.models import User
from .forms import UserInviteCreateForm, TeamApplyCreateForm
from .access import OnlyYouMixin



""" 通知関連 view """

class UserInviteNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/user_invite_notification.html'

    def get_context_data(self, **kwargs):

        """
            ユーザーに送った招待が承認・拒否された場合に通知
        """
        if self.request.user.is_owner == True:
            ctx = super().get_context_data(**kwargs)
            ctx['invite'] = Invite.objects.get(user=self.request.user)
            return ctx

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
        ctx = super().get_context_data(**kwargs)
        ctx['apply'] = Apply.objects.get(user=self.request.user)
        return ctx

user_apply_notification = UserApplyNotificationView.as_view()



class UserApplyNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/user_apply_notification_detail.html'
    model = Apply

user_apply_notification_detail = UserApplyNotificationDetailView.as_view()
