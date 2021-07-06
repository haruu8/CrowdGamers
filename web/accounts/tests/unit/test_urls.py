from django.test import TestCase, Client
from django.urls import resolve, reverse
from accounts.views import *


class AccountsUrlRoutingTests(TestCase):
    """
    endpointに対して呼び出されるメソッドが正しいかをテストする。
    test_url_resolves_to_*** で関数定義している。
    *** : views の名前
    """
    def test_url_resolves_to_login(self):
        found = resolve('/accounts/login/')
        self.assertEqual(found.func, login)

    def test_url_resolves_to_signup(self):
        found = resolve('/accounts/signup/')
        self.assertEqual(found.func, signup)

    def test_url_resolves_to_logout(self):
        found = resolve('/accounts/logout/')
        self.assertEqual(found.func, logout)

    def test_url_resolves_to_account_delete(self):
        found = resolve('/accounts/hoge/delete/')
        self.assertEqual(found.func, account_delete)

    def test_url_resolves_to_account_settings(self):
        found = resolve('/accounts/settings/')
        self.assertEqual(found.func, account_settings)
