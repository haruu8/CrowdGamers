from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from accounts.models import User
from teams.models import Team, Invite, Apply, UserProfile
from teams.forms import InviteCreateForm, ApplyCreateForm
from teams.views import OnlyYouMixin



""" 通知関連 view """

class InviteNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/invite_notification.html'

    def get_context_data(self, **kwargs):

        """
            ユーザーに送った招待が承認・拒否された場合に通知
        """
        if self.request.user.is_owner == True:
            ctx = super().get_context_data(**kwargs)
            ctx['invite'] = Invite.objects.get(user=self.request.user)
            return ctx

invite_notification = InviteNotificationView.as_view()



class InviteNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/invite_notification_detail.html'
    model = Invite

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.kwargs.get('user'))

invite_notification_detail = InviteNotificationDetailView.as_view()



class ApplyNotificationView(LoginRequiredMixin, OnlyYouMixin, TemplateView):
    template_name = 'teams/notification/apply_notification.html'

    def get_context_data(self, **kwargs):

        """
            クランに送ったリクエストの承認可否
        """
        ctx = super().get_context_data(**kwargs)
        ctx['apply'] = Apply.objects.get(user=self.request.user)
        return ctx

apply_notification = ApplyNotificationView.as_view()



class ApplyNotificationDetailView(LoginRequiredMixin, OnlyYouMixin, DetailView):
    template_name = 'teams/notification/apply_notification_detail.html'
    model = Apply

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.kwargs.get('user'))

apply_notification_detail = ApplyNotificationDetailView.as_view()
