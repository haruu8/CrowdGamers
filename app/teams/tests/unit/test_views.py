from django.test import TestCase, RequestFactory
from unittest.mock import MagicMock, patch
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from teams.views.team import TeamCreateView


# Django の view は親クラスとの依存が強いので、
# このクラスを挟むことで依存をなるべく取り除く
# 慣れてきたらライブラリを使って似たようなことをやるといい
class InjectableTeamCreateView(TeamCreateView):

    # form_valid_for_create_view が返す response をモックする
    def inject_success_response(self, response):
        self.__success_response = response

    # super().form_valid がモックしづらいので、ここで上書きする
    def form_valid_for_create_view(self, form):
        return self.__success_response

    # request を注入できるようにする
    def inject_request(self, request):
        self.request = request

    # team を注入できるようにする
    def inject_object(self, object):
        self.object = object


class TestTeamCreate(TestCase):

    def test_form_valid_user_without_team(self):
        # リクエストをモック
        request_mock = MagicMock()

        # ユーザーはチームには所属していない状態
        request_mock.user.user_profile.team = None

        view = InjectableTeamCreateView()
        view.inject_request(request_mock)

        team_mock = MagicMock()
        view.inject_object(team_mock)

        response_mock = MagicMock()
        view.inject_success_response(response_mock)

        form_mock = MagicMock()
        result = view.form_valid(form_mock)

        # is_owner フラグが立っている
        self.assertTrue(
            request_mock.user.user_profile.is_owner,
            msg="チームの作成者に is_owner フラグが立っていません"
        )
        # team がセットされている
        self.assertEqual(
            team_mock,
            request_mock.user.user_profile.team,
            msg="チーム作成者の所属チームが正しくセットされていません"
        )
        # save されている
        self.assertEqual(
            request_mock.user.user_profile.save.call_count,
            1,
            msg="user_profile が save されていません"
        )

        # 成功レスポンスが返されている
        self.assertEqual(result, response_mock, msg="想定外のレスポンスが返ってきています")
