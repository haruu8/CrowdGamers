from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from teams.models import UserProfile, Team


class UserProfileTests(TestCase):
    """
    username が文字数通りか。(最小値と最大値の境界値テスト)
    required が保存されていれば有効になるか
    """
    def test_user_profile_str(self):
        """
        UserProfile model の str メソッドは username を返す
        """
        user = get_user_model().objects.create_user(
            username='crowdgamers'
        )
        user_profile = user.user_profile
        self.assertEqual(str(user_profile.user.username), "crowdgamers")



class TeamTests(TestCase):
    """
    """
    def test_team_str(self):
        """
        Team model の str メソッドは teamname を返す
        """
        team = baker.make(Team, teamname='hoge')
        self.assertEqual(str(team), 'hoge')
