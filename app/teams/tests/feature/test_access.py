from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from teams.models import Notification, Team



def create_data():
    """
    ステータスコードテストに必要なオブジェクトを共通作成できる関数。
    """
    # ユーザー生成に必要なユーザーを作成
    official = get_user_model().objects.create_user(
        username='crowdgamers',
    )

    # チーム作成
    team = Team.objects.create(
        teamname='hoge',
        name='hoge',
        introduction='hoge',
        desired_condition='hoge',
        disclosed=True,
    )

    # チームオーナー作成
    owner = get_user_model().objects.create_user(
        username='owner',
        password='owner',
    )
    owner_profile = owner.user_profile
    owner_profile.team = team
    owner_profile.desired_condition = 'hoge'
    owner_profile.is_owner = True
    owner_profile.save()

    # チームメンバー作成
    member = get_user_model().objects.create_user(
        username='member',
        password='member',
    )
    member_profile = member.user_profile
    member_profile.team = team
    member_profile.desired_condition = 'hoge'
    member_profile.is_owner = False
    member_profile.save()

    # 無所属ユーザーの作成
    independent_user = get_user_model().objects.create_user(
        username='independent',
        password='independent',
    )

    # 通知オブジェクトの作成
    notification = Notification.objects.create(
        mode='invitation',
        from_user=owner,
        to_user=independent_user,
    )

    # to_user を変更した通知オブジェクトの作成
    notification_to = Notification.objects.create(
        mode='application',
        from_user=independent_user,
        to_user=owner,
    )

    return official, team, owner, owner_profile, member, member_profile, independent_user, notification, notification_to



class TeamAnonymousUserStatusCodeTests(TestCase):
    """
    未ログインユーザーのステータスコードのテスト。
    test_***_status_code で関数定義している。
    *** : urls に登録してる name

    Notes
    -----
    通知部分はオーナー・メンバー・無所属ユーザーの全てのテストを試したいため、命名が異なる。
    test_***_???_status_code
    ??? : アクセスしようとしているユーザーのステータス
    """
    def setUp(self):
        """
        必要なオブジェクトを作成する。
        """
        self.official, self.team, self.owner, self.owner_profile, self.member, self.member_profile, self.independent_user, self.notification, self.notification_to = create_data()

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
        url = reverse('teams:team_update', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_status_code(self):
        """
        team_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_member_status_code(self):
        """
        team_detail_member のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_member', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_feature', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_desired_condition', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_add_status_code(self):
        """
        team_member_add のステータスコードは 302 になる
        """
        url = reverse('teams:team_member_add', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_team_member_list_status_code(self):
        """
        team_member_list のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_list', kwargs={'teamname': self.team})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_member_delete_status_code(self):
        """
        team_member_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_delete', kwargs={'teamname': self.team, 'username': self.owner.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_account_detail_status_code(self):
        """
        account_detail のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_feature', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_desired_condition', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_status_code(self):
        """
        account_profile_update のステータスコードは 403 になる
        """
        url = reverse('teams:account_profile_update', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_team_owner_status_code(self):
        """
        オーナーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_team_member_status_code(self):
        """
        チームメンバーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.member.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_independent_user_status_code(self):
        """
        無所属ユーザーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.independent_user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_detail_status_code(self):
        """
        application_detail のステータスコードは 403 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_detail_status_code(self):
        """
        invitation_detail のステータスコードは 403 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_member_approval_detail_status_code(self):
        """
        member_approval_detail のステータスコードは 403 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_official_detail_status_code(self):
        """
        official_detail のステータスコードは 403 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_create_status_code(self):
        """
        application_create のステータスコードは 302 になる
        """
        url = reverse('teams:application_create', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_application_reply_create_status_code(self):
        """
        application_reply_create のステータスコードは 403 になる
        """
        url = reverse('teams:application_reply_create', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_create_status_code(self):
        """
        team_detail のステータスコードは 302 になる
        """
        url = reverse('teams:invitation_create', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)



class TeamIndependentUserStatusCodeTests(TestCase):
    """
    無所属のログインユーザーのステータスコードのテスト。
    test_***_status_code で関数定義している。
    *** : urls に登録してる name
    """
    def setUp(self):
        """
        必要なオブジェクトを作成する。
        無所属ユーザーでログインをする。
        """
        self.official, self.team, self.owner, self.owner_profile, self.member, self.member_profile, self.independent_user, self.notification, self.notification_to = create_data()
        self.client = Client()
        self.client.login(username='independent', password='independent')

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
        team_create のステータスコードは 200 になる
        """
        url = reverse('teams:team_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

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
        url = reverse('teams:team_update', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_status_code(self):
        """
        team_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_member_status_code(self):
        """
        team_detail_member のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_member', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_feature', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_desired_condition', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_add_status_code(self):
        """
        team_member_add のステータスコードは 302 になる
        """
        url = reverse('teams:team_member_add', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_list_status_code(self):
        """
        team_member_list のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_list', kwargs={'teamname': self.team})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_member_delete_status_code(self):
        """
        team_member_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_delete', kwargs={'teamname': self.team, 'username': self.owner.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_account_detail_status_code(self):
        """
        account_detail のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_feature', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_desired_condition', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_own_status_code(self):
        """
        自分の account_profile_update のステータスコードは 200 になる
        """
        url = reverse('teams:account_profile_update', args=[self.independent_user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_status_code(self):
        """
        他ユーザーの account_profile_update のステータスコードは 403 になる
        """
        url = reverse('teams:account_profile_update', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_team_owner_status_code(self):
        """
        オーナーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_team_member_status_code(self):
        """
        チームメンバーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.member.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_independent_user_status_code(self):
        """
        無所属ユーザーの notification のステータスコードは 200 になる
        """
        url = reverse('teams:notification', args=[self.independent_user.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_application_detail_status_code(self):
        """
        application_detail のステータスコードは 403 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_detail_status_code(self):
        """
        invitation_detail のステータスコードは 403 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_member_approval_detail_status_code(self):
        """
        member_approval_detail のステータスコードは 403 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_official_detail_status_code(self):
        """
        official_detail のステータスコードは 403 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_create_status_code(self):
        """
        application_create のステータスコードは 200 になる
        """
        url = reverse('teams:application_create', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_application_reply_create_status_code(self):
        """
        application_reply_create のステータスコードは 403 になる
        """
        url = reverse('teams:application_reply_create', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_create_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:invitation_create', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)



class TeamMemberUserStatusCodeTests(TestCase):
    """
    チームメンバーユーザーのステータスコードのテスト。
    test_***_status_code で関数定義している。
    *** : urls に登録してる name
    """
    def setUp(self):
        """
        必要なオブジェクトを作成する。
        無所属ユーザーでログインをする。
        """
        self.official, self.team, self.owner, self.owner_profile, self.member, self.member_profile, self.independent_user, self.notification, self.notification_to = create_data()
        self.client = Client()
        self.client.login(username='member', password='member')

    def test_team_create_status_code(self):
        """
        team_create のステータスコードは 200 になる
        """
        url = reverse('teams:team_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

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
        url = reverse('teams:team_update', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_status_code(self):
        """
        team_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_member_status_code(self):
        """
        team_detail_member のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_member', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_feature', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_desired_condition', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_add_status_code(self):
        """
        team_member_add のステータスコードは 200 になる
        """
        url = reverse('teams:team_member_add', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_list_status_code(self):
        """
        team_member_list のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_list', kwargs={'teamname': self.team})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_member_delete_status_code(self):
        """
        team_member_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_delete', kwargs={'teamname': self.team, 'username': self.owner.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_account_detail_status_code(self):
        """
        account_detail のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_feature', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_desired_condition', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_own_status_code(self):
        """
        自分の account_profile_update のステータスコードは 200 になる
        """
        url = reverse('teams:account_profile_update', args=[self.member.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_owner_status_code(self):
        """
        他ユーザーの account_profile_update のステータスコードは 403 になる
        """
        url = reverse('teams:account_profile_update', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_own_status_code(self):
        """
        自分の notification のステータスコードは 200 になる
        """
        url = reverse('teams:notification', args=[self.member.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_application_detail_own_status_code(self):
        """
        自分の application_detail のステータスコードは 200 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_invitation_detail_own_status_code(self):
        """
        自分の invitation_detail のステータスコードは 200 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_member_approval_detail_own_status_code(self):
        """
        自分の member_approval_detail のステータスコードは 200 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_official_detail_own_status_code(self):
        """
        自分の official_detail のステータスコードは 200 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_notification_owner_status_code(self):
        """
        他ユーザーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_detail_owner_status_code(self):
        """
        他ユーザーの application_detail のステータスコードは 403 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_detail_owner_status_code(self):
        """
        他ユーザーの invitation_detail のステータスコードは 403 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_member_approval_detail_owner_status_code(self):
        """
        他ユーザーの member_approval_detail のステータスコードは 403 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_official_detail_owner_status_code(self):
        """
        他ユーザーの official_detail のステータスコードは 403 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_create_status_code(self):
        """
        application_create のステータスコードは 200 になる
        """
        url = reverse('teams:application_create', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_application_reply_create_status_code(self):
        """
        application_reply_create のステータスコードは 403 になる
        """
        url = reverse('teams:application_reply_create', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_create_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:invitation_create', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)



class TeamOwnerUserStatusCodeTests(TestCase):
    """
    オーナーユーザーのステータスコードのテスト。
    test_***_status_code で関数定義している。
    *** : urls に登録してる name
    """
    def setUp(self):
        """
        必要なオブジェクトを作成する。
        無所属ユーザーでログインをする。
        """
        self.other_team = Team.objects.create(
            teamname='hogehoge',
            name='hogehoge',
            introduction='hogehoge',
            desired_condition='hogehoge',
            disclosed=True,
        )
        self.official, self.team, self.owner, self.owner_profile, self.member, self.member_profile, self.independent_user, self.notification, self.notification_to = create_data()
        self.client = Client()
        self.client.login(username='owner', password='owner')

    def test_team_create_status_code(self):
        """
        team_create のステータスコードは 200 になる
        """
        url = reverse('teams:team_create')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_list_status_code(self):
        """
        team_list のステータスコードは 200 になる
        """
        url = reverse('teams:team_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_update_own_status_code(self):
        """
        自チームの team_update のステータスコードは 200 になる
        """
        url = reverse('teams:team_update', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_update_other_team_status_code(self):
        """
        他チームの team_update のステータスコードは 403 になる
        """
        url = reverse('teams:team_update', args=[self.other_team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_delete_own_status_code(self):
        """
        自チームの team_delete のステータスコードは 200 になる
        """
        url = reverse('teams:team_delete', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_delete_other_team_status_code(self):
        """
        他チームの team_delete のステータスコードは 403 になる
        """
        url = reverse('teams:team_delete', args=[self.other_team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_detail_status_code(self):
        """
        team_detail のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_member_status_code(self):
        """
        team_detail_member のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_member', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_feature', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:team_detail_desired_condition', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_add_status_code(self):
        """
        team_member_add のステータスコードは 200 になる
        """
        url = reverse('teams:team_member_add', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_list_own_status_code(self):
        """
        自チームの team_member_list のステータスコードは 200 になる
        """
        url = reverse('teams:team_member_list', kwargs={'teamname': self.team})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_team_member_list_other_team_status_code(self):
        """
        他チームの team_member_list のステータスコードは 403 になる
        """
        url = reverse('teams:team_member_list', kwargs={'teamname': self.other_team})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_team_member_delete_status_code(self):
        """
        team_member_delete のステータスコードは 200 になる
        """
        url = reverse('teams:team_member_delete', kwargs={'teamname': self.team, 'username': self.member.username})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_status_code(self):
        """
        account_detail のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_feature_status_code(self):
        """
        team_detail_feature のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_feature', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_detail_desired_condition_status_code(self):
        """
        team_detail_desired_condition のステータスコードは 200 になる
        """
        url = reverse('teams:account_detail_desired_condition', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_own_status_code(self):
        """
        自分の account_profile_update のステータスコードは 200 になる
        """
        url = reverse('teams:account_profile_update', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_account_profile_update_member_status_code(self):
        """
        他ユーザーの account_profile_update のステータスコードは 403 になる
        """
        url = reverse('teams:account_profile_update', args=[self.member.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_notification_own_status_code(self):
        """
        自分の notification のステータスコードは 200 になる
        """
        url = reverse('teams:notification', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_application_detail_own_from_user_status_code(self):
        """
        自分が from_user の application_detail のステータスコードは 302 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_invitation_detail_own_from_user_status_code(self):
        """
        自分が from_user の invitation_detail のステータスコードは 302 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_member_approval_detail_own_from_user_status_code(self):
        """
        自分が from_user の member_approval_detail のステータスコードは 302 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_application_detail_own_to_user_status_code(self):
        """
        自分が to_user の application_detail のステータスコードは 200 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.owner.username, 'id': self.notification_to.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_invitation_detail_own_to_user_status_code(self):
        """
        自分が to_user の invitation_detail のステータスコードは 200 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.owner.username, 'id': self.notification_to.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_member_approval_detail_own_to_user_status_code(self):
        """
        自分が to_user の member_approval_detail のステータスコードは 200 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.owner.username, 'id': self.notification_to.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_official_detail_own_status_code(self):
        """
        自分の official_detail のステータスコードは 200 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_notification_owner_status_code(self):
        """
        他ユーザーの notification のステータスコードは 403 になる
        """
        url = reverse('teams:notification', args=[self.member.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_detail_owner_status_code(self):
        """
        他ユーザーの application_detail のステータスコードは 403 になる
        """
        url = reverse('teams:application_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_invitation_detail_owner_status_code(self):
        """
        他ユーザーの invitation_detail のステータスコードは 403 になる
        """
        url = reverse('teams:invitation_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_member_approval_detail_owner_status_code(self):
        """
        他ユーザーの member_approval_detail のステータスコードは 403 になる
        """
        url = reverse('teams:member_approval_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_official_detail_owner_status_code(self):
        """
        他ユーザーの official_detail のステータスコードは 403 になる
        """
        url = reverse('teams:official_detail', kwargs={'username': self.member.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def test_application_create_status_code(self):
        """
        application_create のステータスコードは 200 になる
        """
        url = reverse('teams:application_create', args=[self.team])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_application_reply_create_own_status_code(self):
        """
        自分の application_reply_create のステータスコードは 200 になる
        """
        url = reverse('teams:application_reply_create', kwargs={'username': self.owner.username, 'id': self.notification.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_invitation_create_status_code(self):
        """
        invitation_create のステータスコードは 200 になる
        """
        url = reverse('teams:invitation_create', args=[self.owner.username])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
