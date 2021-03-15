from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
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



class AccountsStatusCodeTests(TestCase):
    """
    ステータスコードのテスト。
    test_***_status_code_???_user で関数定義している。
    *** : urls に登録してる name
    ??? : ユーザーの状態を示す

    See Also
    --------
    関数定義の ??? の部分の命名
    anonymous : 未ログインユーザー
    authenticated : ログインユーザー
    """
    def setUp(self):
        """
        アクセスパーミションテストに必要なオブジェクトを作成する。

        See Also
        --------
        user : object
            User モデルのオブジェクト。
        """
        self.user = get_user_model().objects.create_user(
            username='CrowdGamers',
        )
        self.client = Client()

    def test_account_login_status_code_anonymous_user(self):
            """
            account_login のステータスコードは 200 になる
            """
            url = reverse('accounts:account_login')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_account_signup_status_code_anonymous_user(self):
            """
            account_signup のステータスコードは 200 になる
            """
            url = reverse('accounts:account_signup')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_account_logout_status_code_anonymous_user(self):
            """
            account_logout のステータスコードは 200 になる
            """
            url = reverse('accounts:account_logout')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_account_delete_status_code_anonymous_user(self):
            """
            account_delete のステータスコードは 403 になる
            """
            url = reverse('accounts:account_delete', args=[self.user.username])
            response = self.client.get(url)
            self.assertEquals(response.status_code, 403)

    def test_account_settings_status_code_anonymous_user(self):
            """
            account_settings のステータスコードは 302 になる
            """
            url = reverse('accounts:account_settings')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 302)

    """ ここからログイン時のテスト """

    def test_account_login_status_code_authenticated_user(self):
            """
            account_login のステータスコードは 200 になる
            """
            self.client.login(usenrame='CrowdGamers')
            url = reverse('accounts:account_login')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_account_signup_status_code_authenticated_user(self):
            """
            account_signup のステータスコードは 200 になる
            """
            self.client.login(usenrame='CrowdGamers')
            url = reverse('accounts:account_signup')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_account_logout_status_code_authenticated_user(self):
            """
            account_logout のステータスコードは 200 になる
            """
            self.client.login(usenrame='CrowdGamers')
            url = reverse('accounts:account_logout')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_account_delete_status_code_authenticated_user(self):
            """
            account_delete のステータスコードは 403 になる
            """
            self.client.login(usenrame='CrowdGamers')
            url = reverse('accounts:account_delete', args=[self.user.username])
            response = self.client.get(url)
            self.assertEquals(response.status_code, 403)

    def test_account_settings_status_code_authenticated_user(self):
            """
            account_settings のステータスコードは 302 になる
            """
            self.client.login(usenrame='CrowdGamers')
            url = reverse('accounts:account_settings')
            response = self.client.get(url)
            self.assertEquals(response.status_code, 302)
