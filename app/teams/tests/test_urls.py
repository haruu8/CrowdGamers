from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from teams.models import Team, UserProfile, Notification
from teams.views import *



class TeamUrlRoutingTests(TestCase):
    """
    endpointに対して呼び出されるメソッドが正しいか

    Notes
    -----
    test_url_resolves_to_*** で関数定義している。 *** は views の名前
    """
    def setUp(self):
        pass

    def test_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEqual(found.func, home)



class TeamStatusCodeTests(TestCase):
    """
    test_***_status_code_???_user で関数定義しているステータスコードのテスト
    *** : urls に登録してる name
    ??? : ユーザーの状態を示す

    See Also
    --------
    関数定義の ??? の部分の命名
    anonymous : 未ログインユーザー
    authenticated_independent : ログインユーザー（チーム無所属）
    authenticated_team_member : ログインユーザー（チーム所属、自身のチームへのテスト）
    authenticated_another_team_member : ログインユーザー（チーム所属、他チームへのテスト）
    authenticated_team_owner : ログインユーザー（チームオーナー、自身のチームへのテスト）
    authenticated_another_team_owner : ログインユーザー（チームオーナー、他チームへのテスト）
    """
    def setUp(self):
        """
        アクセスパーミションテストに必要なオブジェクトを作成する

        Parameters
        ----------
        team : object
            Team モデルのオブジェクト
        user : object
            User モデルのオブジェクト
        profile : object
            UserProfile モデルのオブジェクト
        notification : object
            Notification モデルのオブジェクト
        """
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
        self.profile = self.user.user_profile
        self.profile.team = self.team
        self.profile.desired_condition = 'hoge'
        self.profile.is_owner=True
        self.notification = Notification.objects.create(
            mode='official',
            from_user=self.user,
            to_user=self.user,
        )
        self.client = Client()

    def test_home_status_code_anonymous_user(self):
        """
        home のステータスコードは 200 になる
        """
        url = reverse('teams:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_contact_status_code_anonymous_user(self):
        """
        contact のステータスコードは 200 になる
        """
        url = reverse('teams:contact')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_faq_status_code_anonymous_user(self):
        """
        faq のステータスコードは 200 になる
        """
        url = reverse('teams:faq')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_terms_of_service_status_code_anonymous_user(self):
        """
        terms_of_service のステータスコードは 200 になる
        """
        url = reverse('teams:terms_of_service')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_privacy_policy_status_code_anonymous_user(self):
        """
        privacy_policy のステータスコードは 200 になる
        """
        url = reverse('teams:privacy_policy')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_accounts_list_status_code_anonymous_user(self):
        """
        accounts_list のステータスコードは 200 になる
        """
        url = reverse('teams:accounts_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_create_status_code_anonymous_user(self):
        """
        team_create のステータスコードは 302 になる
        """
        url = reverse('teams:team_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_team_list_status_code_anonymous_user(self):
        """
        team_list のステータスコードは 200 になる
        """
        url = reverse('teams:team_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_update_status_code_anonymous_user(self):
        """
        team_update のステータスコードは 403 になる
        """
        url = reverse('teams:team_update', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_status_code_anonymous_user(self):
        """
        team_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code_anonymous_user(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # def test_team_detail_member_status_code_anonymous_user(self):
    #     """
    #     TODO
    #     ----
    #     修正する
    #     """
    #     url = reverse('teams:team_detail_member', args=[self.team])
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)

    def test_team_detail_feature_status_code_anonymous_user(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_feature', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_desired_condition_status_code_anonymous_user(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_desired_condition', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_add_status_code_anonymous_user(self):
        """
        team_member_add のステータスコードは 302 になる
        """
        url = reverse('teams:team_member_add', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_team_member_delete_status_code_anonymous_user(self):
        """
        team_member_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_delete', kwargs={'teamname': self.team, 'username': self.user.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_account_detail_status_code_anonymous_user(self):
        """
        account_detail のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail', args=[self.user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_feature_status_code_anonymous_user(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_feature', args=[self.user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_desired_condition_status_code_anonymous_user(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_desired_condition', args=[self.user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_status_code_anonymous_user(self):
        """
        account_profile_update のステータスコードは 403 になる
        """
        url = reverse('teams:account_profile_update', args=[self.user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_status_code_anonymous_user(self):
        """
        notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_detail_status_code_anonymous_user(self):
        """
        application_detail のステータスコードは 403 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.user.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_detail_status_code_anonymous_user(self):
        """
        invitation_detail のステータスコードは 403 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.user.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_member_approval_detail_status_code_anonymous_user(self):
        """
        member_approval_detail のステータスコードは 403 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.user.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_official_detail_status_code_anonymous_user(self):
        """
        official_detail のステータスコードは 403 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.user.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_create_status_code_anonymous_user(self):
        """
        application_create のステータスコードは 302 になる
        """
        url = reverse('teams:application_create', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_application_reply_create_status_code_anonymous_user(self):
        """
        application_reply_create のステータスコードは 403 になる
        """
        url = reverse('teams:application_reply_create', kwargs={'username': self.user.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_create_status_code_anonymous_user(self):
        """
        team_detail のステータスコードは 302 になる
        """
        url = reverse('teams:invitation_create', args=[self.user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

# class TeamHtmlTests(TestCase):
#     """
#     endpointに対して使われるテンプレート(html)が正しいか
#     """
#     def test_home_html(self):
#         request = HttpRequest()
#         response = home(request)
#         expected_html = render_to_string('teams/home.html')
#         self.assertEqual(response.content.decode(), expected_html)
