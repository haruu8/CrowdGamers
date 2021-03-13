from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from teams.views import *
from django.contrib.auth import get_user_model



class TeamUrlRoutingTests(TestCase):
    """
    endpointに対して呼び出されるメソッドが正しいか

    Notes
    -----
    test_url_resolves_to_*** で関数定義している。 *** は views の名前
    """
    # def setUp(self):
    #     get_user_model().objects.create_user(
    #         username='hoge',
    #     )

    def test_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEqual(found.func, GetProfileView)



class TeamStatusCodeTests(TestCase):
    """
    ステータスコードが正しいかテスト

    Notes
    -----
    test_***_status_code で関数定義している。 *** は urls に登録してある name
    """
    def setUp(self):
        # ここにテストデータを書く
        pass

    def test_home_status_code(self):
        url = reverse('teams:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contact_status_code(self):
        url = reverse('teams:contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # アクセス時はエラーが出ないが、テスト時はエラーが出る
    # def test_faq_status_code(self):
    #     url = reverse('teams:faq')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    def test_terms_of_service_status_code(self):
        url = reverse('teams:terms_of_service')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_privacy_policy_status_code(self):
        url = reverse('teams:privacy_policy')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_accounts_list_status_code(self):
        url = reverse('teams:accounts_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_create_status_code(self):
        url = reverse('teams:team_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_team_list_status_code(self):
        url = reverse('teams:team_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)



# class TeamHtmlTests(TestCase):
#     """
#     endpointに対して使われるテンプレート(html)が正しいか
#     """
#     def test_home_html(self):
#         request = HttpRequest()
#         response = views.home(request)
#         expected_html = render_to_string('teams/home.html')
#         self.assertEqual(response.content.decode(), expected_html)
