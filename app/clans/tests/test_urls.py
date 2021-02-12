from django.test import TestCase
from django.core.urlresolvers import resolve
from . import views
from accounts.models import User
from django.http import HttpRequest
from django.template.loader import render_to_string



""" 正しい View が呼び出されているかテスト """

class ClanUrlRoutingTests(TestCase):

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

    def test_url_resolves_to_clan_create(self):
        found = resolve('clan/create/')
        self.assertEqual(found.func, views.clan_create)

    def test_url_resolves_to_clan_list(self):
        found = resolve('clan/list/')
        self.assertEqual(found.func, views.clan_list)

    # 詳細画面のテストコードの書き方
    def test_url_resolves_to_clan_detail(self):
        found = resolve('clan/<str:name>/')
        self.assertEqual(found.func, views.clan_detail)



""" 正しい HTML が返されているかテスト """

class ClanHtmlTests(TestCase):

    def test_home_html(self):
        request = HttpRequest()
        response = views.home(request)
        expected_html = render_to_string('clans/home.html')
        self.assertEqual(response.content.decode(), expected_html)
