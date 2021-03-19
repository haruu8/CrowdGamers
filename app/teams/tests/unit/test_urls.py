from unittest.mock import MagicMock, patch
from django.test import TestCase, Client, RequestFactory
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from teams.models import Team, UserProfile, Notification
from teams.views import *



class TeamUrlRoutingTests(TestCase):
    """
    endpointに対して呼び出されるメソッドが正しいかをテストする。
    test_url_resolves_to_*** で関数定義している。
    *** : views の名前
    """
    def test_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_url_resolves_to_contact(self):
        found = resolve('/contact/')
        self.assertEqual(found.func, contact)

    def test_url_resolves_to_faq(self):
        found = resolve('/faq/')
        self.assertEqual(found.func, faq)

    def test_url_resolves_to_terms_of_service(self):
        found = resolve('/terms_of_service/')
        self.assertEqual(found.func, terms_of_service)

    def test_url_resolves_to_privacy_policy(self):
        found = resolve('/privacy_policy/')
        self.assertEqual(found.func, privacy_policy)

    def test_url_resolves_to_accounts_list(self):
        found = resolve('/accounts/list/')
        self.assertEqual(found.func, accounts_list)

    def test_url_resolves_to_team_create(self):
        found = resolve('/team/create/')
        self.assertEqual(found.func, team_create)

    def test_url_resolves_to_team_create(self):
        found = resolve('/team/hoge/update/')
        self.assertEqual(found.func, team_update)

    def test_url_resolves_to_team_delete(self):
        found = resolve('/team/hoge/delete/')
        self.assertEqual(found.func, team_delete)

    def test_url_resolves_to_team_detail(self):
        found = resolve('/team/hoge/')
        self.assertEqual(found.func, team_detail)

    def test_url_resolves_to_team_detail_member(self):
        found = resolve('/team/hoge/member/')
        self.assertEqual(found.func, team_detail_member)

    def test_url_resolves_to_team_detail_feature(self):
        found = resolve('/team/hoge/feature/')
        self.assertEqual(found.func, team_detail_feature)

    def test_url_resolves_to_team_detail_desired_condition(self):
        found = resolve('/team/hoge/desired_condition/')
        self.assertEqual(found.func, team_detail_desired_condition)

    def test_url_resolves_to_team_member_add(self):
        found = resolve('/team/hoge/member/add/')
        self.assertEqual(found.func, team_member_add)

    def test_url_resolves_to_team_member_delete(self):
        found = resolve('/team/hoge/member/delete/hoge/')
        self.assertEqual(found.func, team_member_delete)

    def test_url_resolves_to_account_detail(self):
        found = resolve('/hoge/')
        self.assertEqual(found.func, account_detail)

    def test_url_resolves_to_account_detail_feature(self):
        found = resolve('/hoge/feature/')
        self.assertEqual(found.func, account_detail_feature)

    def test_url_resolves_to_account_detail_desired_condition(self):
        found = resolve('/hoge/desired_condition/')
        self.assertEqual(found.func, account_detail_desired_condition)

    def test_url_resolves_to_account_profile_update(self):
        found = resolve('/hoge/update/')
        self.assertEqual(found.func, account_profile_update)

    def test_url_resolves_to_notification(self):
        found = resolve('/hoge/notification/')
        self.assertEqual(found.func, notification)

    def test_url_resolves_to_notification_application_detail(self):
        found = resolve('/hoge/notification/application/16fd2706-8baf-433b-82eb-8c7fada847da/')
        self.assertEqual(found.func, application_detail)

    def test_url_resolves_to_notification_invitation_detail(self):
        found = resolve('/hoge/notification/invitation/16fd2706-8baf-433b-82eb-8c7fada847da/')
        self.assertEqual(found.func, invitation_detail)

    def test_url_resolves_to_notification_member_approval_detail(self):
        found = resolve('/hoge/notification/member_approval/16fd2706-8baf-433b-82eb-8c7fada847da/')
        self.assertEqual(found.func, member_approval_detail)

    def test_url_resolves_to_notification_official_detail(self):
        found = resolve('/hoge/notification/official/16fd2706-8baf-433b-82eb-8c7fada847da/')
        self.assertEqual(found.func, official_detail)

    def test_url_resolves_to_application_create(self):
        found = resolve('/team/hoge/application/create/')
        self.assertEqual(found.func, application_create)

    def test_url_resolves_to_application_reply_create(self):
        found = resolve('/hoge/application/reply/create/16fd2706-8baf-433b-82eb-8c7fada847da/')
        self.assertEqual(found.func, application_reply_create)

    def test_url_resolves_to_invitation_create(self):
        found = resolve('/hoge/invitation/create/')
        self.assertEqual(found.func, invitation_create)



def create_data():
    """
    アクセスパーミションテストに必要なオブジェクトを共通作成できる関数。
    """
    # ユーザー生成に必要なユーザーを作成
    official_mock = MagicMock()
    # チーム作成
    team_mock = MagicMock(teamname='hoge')
    # team_mock.teamname = 'hoge'
    # team_mock.save()
    # チームオーナー作成
    owner_mock = MagicMock()
    # オーナーに必要な設定をする
    owner_mock.user_profile.team = team_mock
    owner_mock.user_profile.is_owner = True
    # 無所属ユーザーの作成
    independent_mock = MagicMock()
    # 通知オブジェクトの生成
    notification_mock = MagicMock()
    # notification の設定をする
    return official_mock, team_mock, owner_mock, notification_mock, independent_mock



class TeamAnonymousUserStatusCodeTests(TestCase):
    def setUp(self):
        self.official_mock, self.team_mock, self.owner_mock, self.notification_mock, self.independent_mock = create_data()

    def test_home_status_code(self):
        """
        home のステータスコードは 200 になる
        """
        url = reverse('teams:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contact_status_code(self):
        """
        contact のステータスコードは 200 になる
        """
        url = reverse('teams:contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_faq_status_code(self):
        """
        faq のステータスコードは 200 になる
        """
        url = reverse('teams:faq')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_terms_of_service_status_code(self):
        """
        terms_of_service のステータスコードは 200 になる
        """
        url = reverse('teams:terms_of_service')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_privacy_policy_status_code(self):
        """
        privacy_policy のステータスコードは 200 になる
        """
        url = reverse('teams:privacy_policy')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_accounts_list_status_code(self):
        """
        accounts_list のステータスコードは 200 になる
        """
        url = reverse('teams:accounts_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_create_status_code(self):
        """
        team_create のステータスコードは 302 になる
        """
        url = reverse('teams:team_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_team_list_status_code(self):
        """
        team_list のステータスコードは 200 になる
        """
        url = reverse('teams:team_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_update_status_code(self):
        """
        team_update のステータスコードは 403 になる
        """
        url = reverse('teams:team_update', args=[self.team_mock])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_status_code(self):
        """
        team_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_delete', args=[self.team_mock])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail', args=[self.team_mock.teamname])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # def test_team_detail_member_status_code(self):
    #     """
    #     team_detail_member のステータスコードは 200 になる
    #     """
    #     url = reverse('teams:team_detail_member', args=[self.team_mock])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_team_detail_feature_status_code(self):
    #     """
    #     team_detail_feature のステータスコードは 200 になる
    #     """
    #     url = reverse('teams:team_detail_feature', args=[self.team_mock])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_team_detail_desired_condition_status_code(self):
    #     """
    #     team_detail_desired_condition のステータスコードは 200 になる
    #     """
    #     url = reverse('teams:team_detail_desired_condition', args=[self.team_mock])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_team_member_add_status_code(self):
    #     """
    #     team_member_add のステータスコードは 302 になる
    #     """
    #     url = reverse('teams:team_member_add', args=[self.team_mock])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 302)

    # def test_team_member_list_status_code(self):
    #     """
    #     team_member_list のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:team_member_list', args=[self.team_mock])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_team_member_delete_status_code(self):
    #     """
    #     team_member_delete のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:team_member_delete', kwargs={'teamname': self.team_mock, 'username': self.owner_mock.username})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_account_detail_status_code(self):
    #     """
    #     account_detail のステータスコードは 200 になる
    #     """
    #     url = reverse('teams:account_detail', args=[self.owner_mock.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_account_detail_feature_status_code(self):
    #     """
    #     team_detail_feature のステータスコードは 200 になる
    #     """
    #     url = reverse('teams:account_detail_feature', args=[self.owner_mock.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_account_detail_desired_condition_status_code(self):
    #     """
    #     team_detail_desired_condition のステータスコードは 200 になる
    #     """
    #     url = reverse('teams:account_detail_desired_condition', args=[self.owner_mock.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    # def test_account_profile_update_status_code(self):
    #     """
    #     account_profile_update のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:account_profile_update', args=[self.owner_mock.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_notification_team_owner_status_code(self):
    #     """
    #     オーナーの notification のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:notification', args=[self.owner_mock.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_notification_team_member_status_code(self):
    #     """
    #     チームメンバーの notification のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:notification', args=[self.member.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_notification_independent_user_status_code(self):
    #     """
    #     無所属ユーザーの notification のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:notification', args=[self.independent_user.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_application_detail_status_code(self):
    #     """
    #     application_detail のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:application_detail', kwargs={'username': self.owner_mock.username, 'id': self.notification_mock.id})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_invitation_detail_status_code(self):
    #     """
    #     invitation_detail のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:invitation_detail', kwargs={'username': self.owner_mock.username, 'id': self.notification_mock.id})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_member_approval_detail_status_code(self):
    #     """
    #     member_approval_detail のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:member_approval_detail', kwargs={'username': self.owner_mock.username, 'id': self.notification_mock.id})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_official_detail_status_code(self):
    #     """
    #     official_detail のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:official_detail', kwargs={'username': self.owner_mock.username, 'id': self.notification_mock.id})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_application_create_status_code(self):
    #     """
    #     application_create のステータスコードは 302 になる
    #     """
    #     url = reverse('teams:application_create', args=[self.team_mock])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 302)

    # def test_application_reply_create_status_code(self):
    #     """
    #     application_reply_create のステータスコードは 403 になる
    #     """
    #     url = reverse('teams:application_reply_create', kwargs={'username': self.owner_mock.username, 'id': self.notification_mock.id})
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 403)

    # def test_invitation_create_status_code(self):
    #     """
    #     team_detail のステータスコードは 302 になる
    #     """
    #     url = reverse('teams:invitation_create', args=[self.owner_mock.username])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 302)
