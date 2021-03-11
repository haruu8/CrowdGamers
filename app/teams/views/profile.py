from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib import messages
from django.contrib.auth import get_user_model
from .access import OnlyYouMixin
from teams.models import Notification, UserProfile
from teams.forms import UserProfileUpdateForm



class UserProfileBaseView(DetailView):
    """
    ユーザープロフィールのデータを取得する
    """
    template_name = 'teams/accounts/profile_extends_base.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))


class UserProfileDetailGameView(UserProfileBaseView):
    """
    プロフィール下段のゲームを表示する
    """
    template_name = 'teams/accounts/account_detail_game.html'
    model = UserProfile

account_detail_game = UserProfileDetailGameView.as_view()



class UserProfileDetailFeatureView(UserProfileBaseView):
    """
    プロフィール下段の特徴を表示する
    """
    template_name = 'teams/accounts/account_detail_feature.html'
    model = UserProfile

account_detail_feature = UserProfileDetailFeatureView.as_view()



class UserProfileDetailDesiredConditionView(UserProfileBaseView):
    """
    プロフィール下段の希望条件を表示する
    """
    template_name = 'teams/accounts/account_detail_desired_condition.html'
    model = UserProfile

account_detail_desired_condition = UserProfileDetailDesiredConditionView.as_view()



class UserProfileUpdateView(OnlyYouMixin, UpdateView):
    """
    プロフィールを更新する
    """
    template_name = 'teams/accounts/account_profile_update.html'
    model = UserProfile
    form_class = UserProfileUpdateForm
    success_url = 'teams:account_detail'

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object = UserProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.user_profile)
        self.object.save()
        return result

    def get_success_url(self):
        return resolve_url(self.success_url, username=self.kwargs.get('username'))

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

account_profile_update = UserProfileUpdateView.as_view()



class UserListView(ListView):
    """
    ユーザーの一覧表示・検索を行う

    Notes
    -----
    User モデルでの検索ではなく、 UserProfile での検索

    TODO
    -----
    html を編集する
    """
    template_name = 'teams/accounts/accounts_list.html'
    model = UserProfile

    def get_queryset(self):
        queryset = UserProfile.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                            Q(name__icontains=keyword) |
                            Q(description__icontains=keyword)
                        )
            messages.success(self.request, '「{}」の検索結果'.format(keyword))

        return queryset

accounts_list = UserListView.as_view()
