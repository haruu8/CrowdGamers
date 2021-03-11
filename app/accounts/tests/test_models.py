from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.model = get_user_model()
        cls.user = get_user_model().objects.create(
            username='hoge',
        )

    def test_min_length(self):
        """
        最小文字数の境界値テスト
        """
        self.assertEqual(self.user)

    def test_max_length(self):
        """
        最大文字数の境界値テスト
        """
        pass
