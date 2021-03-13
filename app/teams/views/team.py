from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from functools import reduce
from operator import and_
from teams.models import Team, UserProfile, Notification
from teams.forms import TeamCreateForm, MemberApprovalCreateForm
from .access import OnlyYouMixin, OnlyOwnerMixin
from .utils import GetProfileView
from .profile import UserProfileBaseView



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid(self, form):
        """
        チームに所属してなければ作成できる validation つきの保存処理

        Notes
        -----
        作成時はデフォルトでオーナー
        """
        profile = self.request.user.user_profile
        if profile.team:
            form.add_error(None, 'チームは1つまでしか所属できません。')
            return render(self.request, self.template_name, {'form': form})
        result = super().form_valid(form)
        profile.is_owner = True
        profile.team = self.object
        profile.save()
        return result

    def get_success_url(self):
        return reverse('teams:team_detail', kwargs={'teamname': self.object.teamname})

team_create = TeamCreateView.as_view()



class TeamListView(ListView):
    """
    チームを検索する

    Notes
    -----
    仕組みは UserListView と変わらない
    """
    template_name = 'teams/team_list.html'
    model = Team

    def get_queryset(self):
        """
        検索の処理

        See Also
        --------
        keyword : html検索バーから受け取った文字列

        Notes
        -----
        仕組みは TeamListView と同じ
        """
        queryset = Team.objects.order_by('-created_at')
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
                                    Q(teamname__icontains=q) |
                                    Q(introduction__icontains=q) |
                                    Q(desired_condition__icontains=q)
                                    for q in q_list])
            queryset = queryset.filter(query)
            # messages.success(self.request, '「{}」の検索結果'.format(keyword))
        return queryset

team_list = TeamListView.as_view()



class TeamUpdateView(LoginRequiredMixin, OnlyOwnerMixin, UpdateView):
    """
    チームプロフィールをアップデートする

    Notes
    -----
    teamname を変更したら URL が Not found になるため success_url は teamname の関係ない URL にする
    """
    template_name = 'teams/team_update.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_update = TeamUpdateView.as_view()



class TeamDeleteView(LoginRequiredMixin, OnlyOwnerMixin, TemplateView):
    """
    チームを削除する

    Notes
    -----
    buttonを使用するので TemplateView の post をオーバーライドする
    """
    template_name = 'teams/team_delete.html'
    success_url = 'teams:home'

    def post(self, request, *args, **kwargs):
        """
        削除・削除キャンセルの処理
        """
        self.object = Team.objects.get(teamname=self.kwargs.get('teamname'))
        if self.request.POST.get('confirm', '') == 'delete':
            user_profile = self.request.user.user_profile
            user_profile.is_owner = False
            user_profile.save()
            self.object.delete()
        elif self.request.POST.get('confirm', '') == 'back':
            return redirect('teams:team_update', teamname=self.kwargs.get('teamname'))
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """
        確認用に見れるようにデータ取得
        """
        ctx = super().get_context_data(**kwargs)
        ctx['team'] = Team.objects.get(teamname=self.kwargs.get('teamname'))
        return ctx

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_delete = TeamDeleteView.as_view()



class TeamDetailBaseView(DetailView):
    """
    チームプロフィールの共通部分を表示する

    Notes
    -----
    member 以外の情報はここで全て取得している
    """
    template_name = 'teams/team_detail.html'
    model = Team
    context_object_name = 'team'

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)



class TeamDetailGameView(TeamDetailBaseView):
    """
    プロフィール下段のゲームを表示する
    """
    template_name = 'teams/team_profile/team_detail.html'
    model = Team

team_detail = TeamDetailGameView.as_view()



class TeamDetailMemberView(TeamDetailBaseView):
    """
    プロフィール下段のメンバーを表示する
    """
    template_name = 'teams/team_profile/team_detail_member.html'
    model = Team

    def get_context_data(self, **kwargs):
        """
        チームに所属しているメンバーを取得する

        Notes
        -----
        owner_profile で一括で取得しようとするとできないので必要なオブジェクトのみ取得
        """
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, teamname=self.kwargs.get("teamname"))
        owner_profile = team.belonging_user_profiles.filter(is_owner=True)[0]
        context['owner_profile_user_username'] = owner_profile.user.username
        context['owner_profile_icon_url'] = owner_profile.icon.url
        context['owner_profile_name'] = owner_profile.name

        member_profile = UserProfile.objects.filter(
            team=team,
            is_owner=False,
        )
        context['member_profile'] = member_profile
        return context

team_detail_member = TeamDetailMemberView.as_view()



class TeamDetailFeatureView(TeamDetailBaseView):
    """
    プロフィール下段の特徴を表示する
    """
    template_name = 'teams/team_profile/team_detail_feature.html'
    model = Team

team_detail_feature = TeamDetailFeatureView.as_view()



class TeamDetailDesiredConditionView(TeamDetailBaseView):
    """
    プロフィール下段の希望条件を表示する
    """
    template_name = 'teams/team_profile/team_detail_desired_condition.html'
    model = Team

team_detail_desired_condition = TeamDetailDesiredConditionView.as_view()



class TeamMemberAddView(LoginRequiredMixin, TeamDetailBaseView, CreateView):
    """
    チームのメンバーに追加申請する

    Notes
    -----
    実際の追加処理は申請認可の部分で行う
    -> views/notification.py : MemberApprovalNotificationDetailView
    """
    template_name = 'teams/team_profile/team_member_add.html'
    model = Notification
    form_class = MemberApprovalCreateForm
    success_url = 'teams:team_detail'

    def form_valid(self, form):
        """
        チームのオーナーに通知を送る

        Notes
        -----
        from_user, to_user を設定
        """
        self.object = form.save(commit=False)
        self.object.mode = 'member_approval'
        self.object.from_user = self.request.user

        self.object.team = Team.objects.get(teamname=self.kwargs.get('teamname'))
        member = self.object.team.belonging_user_profiles.all()
        owner_profile = member.filter(is_owner=True)[0]
        self.object.to_user = owner_profile.user
        self.object.save()
        return super().form_valid(form)

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

team_member_add = TeamMemberAddView.as_view()



class TeamMemberDeleteView(OnlyOwnerMixin, UpdateView):
    """
    チームのメンバーから削除する

    Notes
    -----
    オーナーは削除できない
    """
    template_name = 'teams/team_profile/team_member_delete.html'
    model = UserProfile
    success_url = 'teams:team_detail'

    def form_valid(self, form):
        """
        プロフィールの team から削除

        TODO
        -----
        プロフィールのチームを削除する処理を書き加える
        """
        self.object.user_profile = UserProfile.objects.get(user=self.kwargs.get('user'))
        if self.object.user_profile.is_owner == True:
            form.add_error(None, 'チームのオーナーは削除することができません。')
        self.object.user_profile.team = None
        self.object.save()
        result = super().form_valid(form)
        return result

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

team_member_delete = TeamMemberDeleteView.as_view()
