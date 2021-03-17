from django.test import TestCase, Client
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



class TeamAnonymousUserStatusCodeTests(TestCase):
    pass
