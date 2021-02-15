from django.test import TestCase
from django.core.urlresolvers import resolve
from . import views
from accounts.models import User
from django.http import HttpRequest
from django.template.loader import render_to_string



""" 正しい View が呼び出されているかテスト """

class TeamUrlRoutingTests(TestCase):

    # テストユーザー作成方法
    def setUp(self):
        User.objects.create_user(
            username='hogehoge',
            name='ほげ',
            age=12,
        )

    def test_url_resolves_to_home(self):
        found = resolve('')
        self.assertEqual(found.func, views.home)

    def test_url_resolves_to_team_create(self):
        found = resolve('team/create/')
        self.assertEqual(found.func, views.team_create)

    def test_url_resolves_to_team_list(self):
        found = resolve('team/list/')
        self.assertEqual(found.func, views.team_list)

    # 詳細画面のテストコードの書き方
    def test_url_resolves_to_team_detail(self):
        found = resolve('team/<str:team_name>/')
        self.assertEqual(found.func, views.team_detail)



""" 正しい HTML が返されているかテスト """

class TeamHtmlTests(TestCase):

    def test_home_html(self):
        request = HttpRequest()
        response = views.home(request)
        expected_html = render_to_string('teams/home.html')
        self.assertEqual(response.content.decode(), expected_html)
