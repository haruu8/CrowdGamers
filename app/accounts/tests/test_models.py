from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTest(TestCase):
    def setUp(self):
        self.model = get_user_model()
        self.not_min_length_user = get_user_model().objects.create(
            username='hog',
        )
        self.min_length_user = get_user_model().objects.create(
            username='hoge',
        )

    def test_min_length(self):
        """
        最小文字数の境界値テスト
        """
        self.assertEqual(self.min_length_user)

    def test_max_length(self):
        """
        最大文字数の境界値テスト
        """
        pass
