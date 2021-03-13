from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from teams.models import UserProfile
from accounts.models import User



class GetProfileView(TemplateView):
    """
    ヘッダー部分に表示するプロフィール情報を取得する
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        else:
            pass
        return context

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
