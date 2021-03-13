from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from teams.models import Team, UserProfile
from teams.views import *



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
        self.assertEqual(found.func, home)



class TeamStatusCodeTests(TestCase):
    """
    ステータスコードが正しいかテスト

    Notes
    -----
    test_***_status_code で関数定義している。 *** は urls に登録してある name
    """
    def setUp(self):
        self.team = Team.objects.create(
            teamname='hoge',
            name='hoge',
            introduction='hoge',
            desired_condition='hoge',
            disclosed=True,
        )
        self.user = get_user_model().objects.create_user(
            username='CrowdGamers',
        )
        self.user_profile = UserProfile.objects.update_or_create(
            user=self.user,
            team=self.team,
            desired_condition='hoge',
            disclosed=True,
        )

    def test_home_status_code(self):
        url = reverse('teams:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contact_status_code(self):
        url = reverse('teams:contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_faq_status_code(self):
        url = reverse('teams:faq')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

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

    def test_team_update_status_code(self):
        url = reverse('teams:team_update', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_status_code(self):
        url = reverse('teams:team_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code(self):
        url = reverse('teams:team_detail', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # def test_team_detail_member_status_code(self):
    #     url = reverse('teams:team_detail_member', args=[self.team])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    def test_team_detail_feature_status_code(self):
        url = reverse('teams:team_detail_feature', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_desired_condition_status_code(self):
        url = reverse('teams:team_detail_desired_condition', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_add_status_code(self):
        url = reverse('teams:team_member_add', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_delete_status_code(self):
        url = reverse('teams:team_member_delete', kwargs={'teamname': self.team, 'username': self.user})
        # url = reverse('teams:team_member_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_status_code(self):
        url = reverse('teams:account_detail', args=[self.user])
        # url = reverse('teams:team_member_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_feature_status_code(self):
        url = reverse('teams:account_detail_feature', args=[self.user])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_desired_condition_status_code(self):
        url = reverse('teams:account_detail_desired_condition', args=[self.user])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_status_code(self):
        url = reverse('teams:account_profile_update', args=[self.user])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_status_code(self):
        url = reverse('teams:notification', args=[self.user])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)



# class TeamHtmlTests(TestCase):
#     """
#     endpointに対して使われるテンプレート(html)が正しいか
#     """
#     def test_home_html(self):
#         request = HttpRequest()
#         response = views.home(request)
#         expected_html = render_to_string('teams/home.html')
#         self.assertEqual(response.content.decode(), expected_html)
