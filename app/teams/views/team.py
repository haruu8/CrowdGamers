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
from teams.forms import TeamCreateForm, MemberApprovalCreateForm, UserProfileUpdateForm
from .access import OnlyYouMixin, OnlyOwnerMixin
from .utils import GetProfileView
from .profile import UserProfileBaseView



class TeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'teams/team_create.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def form_valid_for_create_view(self, form):
        return super().form_valid(form)

    def form_valid(self, form):
        """
        チームに所属してなければ作成できる validation つきの保存処理。
        作成時はデフォルトでオーナーになる。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            get_success_url で取得した url。
        """
        profile = self.request.user.user_profile
        if profile.team:
            form.add_error(None, 'チームは1つまでしか所属できません。')
            return render(self.request, self.template_name, {'form': form})
        result = self.form_valid_for_create_view(form)
        profile.is_owner = True
        profile.team = self.object
        profile.save()
        return result

    def get_success_url(self):
        """
        保存処理が終わったらリダイレクトする URL を取得する関数。
        """
        return reverse('teams:team_detail', kwargs={'teamname': self.object.teamname})

team_create = TeamCreateView.as_view()



class TeamListView(ListView):
    """
    チームを検索する。
    仕組みは UserListView と変わらない。
    """
    template_name = 'teams/team_list.html'
    model = Team
    paginate_by = 100

    def get_queryset(self):
        """
        検索フォームに keyword が入力されたら、チームモデルから検索をする処理。

        Returns
        -------
        Queryset
            検索ワードによって作られたクエリ。

        See Also
        --------
        keyword : html検索バーから受け取った文字列
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
        return queryset

team_list = TeamListView.as_view()



class TeamUpdateView(LoginRequiredMixin, OnlyOwnerMixin, UpdateView):
    """
    チームプロフィールをアップデートする。

    Notes
    -----
    teamname を変更したら URL が Not found になるため success_url は teamname の関係ない URL にする
    """
    template_name = 'teams/team_update.html'
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy('teams:home')

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_update = TeamUpdateView.as_view()



class TeamDeleteView(LoginRequiredMixin, OnlyOwnerMixin, TemplateView):
    """
    チームを削除する。

    Notes
    -----
    buttonを使用するので TemplateView の post をオーバーライドする。
    """
    template_name = 'teams/team_delete.html'
    success_url = 'teams:home'

    def post(self, request, *args, **kwargs):
        """
        チーム削除・キャンセルの処理をする関数。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            引数に指定した url に redirect。
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
        確認用に見れるようにデータ取得する関数。
        """
        ctx = super().get_context_data(**kwargs)
        ctx['team'] = Team.objects.get(teamname=self.kwargs.get('teamname'))
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

team_delete = TeamDeleteView.as_view()



class TeamDetailBaseView(DetailView):
    """
    チームプロフィールの共通部分を表示する。
    プロフィールの member 以外の情報はここで全て取得している。
    """
    template_name = 'teams/team_detail.html'
    model = Team
    context_object_name = 'team'

    def get_object(self):
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)



class TeamDetailGameView(TeamDetailBaseView):
    """
    プロフィール下段のゲームを表示する。
    """
    template_name = 'teams/team_profile/team_detail.html'
    model = Team

team_detail = TeamDetailGameView.as_view()



class TeamDetailMemberView(TeamDetailBaseView):
    """
    プロフィール下段のメンバーを表示する。
    """
    template_name = 'teams/team_profile/team_detail_member.html'
    model = Team

    def get_context_data(self, **kwargs):
        """
        チームに所属しているメンバーを取得する。

        Returns
        -------
        dict
            オーナー・メンバーの情報入り ctx。

        Notes
        -----
        owner_profile で一括で取得しようとするとできないので必要なオブジェクトのみ取得。
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
    プロフィール下段の特徴を表示する。
    """
    template_name = 'teams/team_profile/team_detail_feature.html'
    model = Team

team_detail_feature = TeamDetailFeatureView.as_view()



class TeamDetailDesiredConditionView(TeamDetailBaseView):
    """
    プロフィール下段の希望条件を表示する。
    """
    template_name = 'teams/team_profile/team_detail_desired_condition.html'
    model = Team

team_detail_desired_condition = TeamDetailDesiredConditionView.as_view()



class TeamMemberAddView(LoginRequiredMixin, TeamDetailBaseView, CreateView):
    """
    チームのメンバーに追加申請する。
    追加処理は申請認可の部分で行う。
    -> ./notification.py : MemberApprovalNotificationDetailView
    """
    template_name = 'teams/team_profile/team_member_add.html'
    model = Notification
    form_class = MemberApprovalCreateForm
    success_url = 'teams:team_detail'

    def form_valid(self, form):
        """
        必要な情報をオブジェクトに登録し、チームのオーナーに通知を送る関数。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            引数に指定した url に redirect もしくは、 get_success_url で指定した url。
        """
        self.object = form.save(commit=False)
        self.object.mode = 'member_approval'
        self.object.team = Team.objects.get(teamname=self.kwargs.get('teamname'))
        if self.request.user.user_profile == self.object.team or self.request.user.user_profile.is_owner is False:
            return redirect(self.success_url, teamname=self.kwargs.get('teamname'))

        self.object.from_user = self.request.user
        member = self.object.team.belonging_user_profiles.all()
        owner_profile = member.filter(is_owner=True)[0]
        self.object.to_user = owner_profile.user
        self.object.save()
        return super().form_valid(form)

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        teamname = self.kwargs.get("teamname")
        return get_object_or_404(Team, teamname=teamname)

    def get_success_url(self):
        """
        form_valid 関数が完了したら、遷移する URL を取得する関数。
        """
        return reverse(self.success_url, kwargs={'teamname': self.object.team.teamname})

team_member_add = TeamMemberAddView.as_view()



class TeamMemberListView(LoginRequiredMixin, OnlyOwnerMixin, TemplateView):
    """
    削除するメンバーを選ぶときに見るメンバーを一覧表示する。
    """
    template_name = 'teams/team_profile/team_member_list.html'

    def get_context_data(self, **kwargs):
        """
        メンバーのデータを取得する関数。

        Returns
        -------
        dict
            メンバーのプロフィール情報入り ctx。
        """
        ctx = super().get_context_data(**kwargs)
        team = Team.objects.get(teamname=self.kwargs.get('teamname'))
        ctx['profiles'] = UserProfile.objects.filter(team=team)
        return ctx

team_member_list = TeamMemberListView.as_view()



class TeamMemberDeleteView(LoginRequiredMixin, OnlyOwnerMixin, DetailView):
    """
    チームのメンバーから削除する。
    """
    template_name = 'teams/team_profile/team_member_delete.html'
    model = get_user_model()

    def post(self, request, *args, **kwargs):
        """
        プロフィールの team から削除。
        オーナーは削除できない。

        Returns
        -------
        Union[HttpResponsePermanentRedirect, HttpResponseRedirect]
            引数に指定した url に redirect。
        """
        user = get_user_model().objects.get(username=self.kwargs.get('username'))
        if user.user_profile.is_owner == True:
            return redirect('teams:home')
        elif self.request.POST.get('approval', '') == 'delete':
            user.user_profile.team = None
            user.user_profile.save()
        return redirect('teams:home')

    def get_context_data(self, **kwargs):
        """
        削除確認のときに表示するユーザー情報を取得する関数。

        Returns
        -------
        dict
            ユーザー情報入り ctx。
        """
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = get_user_model().objects.get(username=self.kwargs.get('username'))
        return ctx

    def get_object(self):
        """
        URL に必要なパラメータを取得する関数。
        """
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username'))

team_member_delete = TeamMemberDeleteView.as_view()
