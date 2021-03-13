from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from functools import reduce
from operator import and_
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
        user = get_user_model().objects.get(username=self.kwargs.get('username'))
        context['user_profile'] = user.user_profile
        return context

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))


class UserProfileDetailGameView(UserProfileBaseView):
    """
    プロフィール下段のゲームを表示する
    """
    template_name = 'teams/accounts/account_detail_game.html'
    model = UserProfile

account_detail = UserProfileDetailGameView.as_view()



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
    template_name = 'teams/accounts/profile_update.html'
    model = UserProfile
    form_class = UserProfileUpdateForm
    success_url = 'teams:account_detail'

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
    UserProfile での検索
    仕組みは TeamListView と同じ
    """
    template_name = 'teams/accounts/accounts_list.html'
    model = UserProfile

    def get_queryset(self):
        """
        検索の処理

        See Also
        --------
        keyword : html検索バーから受け取った文字列
        """
        queryset = UserProfile.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            exclusion = set([' ', '　'])
            q_list = ''
            for i in keyword:
                if i in exclusion:
                    pass
                else:
                    q_list += i
            query = reduce(and_, [Q(name__icontains=q) |
                                    Q(introduction__icontains=q) |
                                    Q(desired_condition__icontains=q)
                                    for q in q_list])
            queryset = queryset.filter(query)
            # messages.success(self.request, '「{}」の検索結果'.format(keyword))
        return queryset

accounts_list = UserListView.as_view()
