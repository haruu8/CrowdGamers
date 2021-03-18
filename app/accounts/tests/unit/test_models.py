from django.test import TestCase
from accounts.models import User



class TestUser(TestCase):
    """
    accounts.models にある関数・クラスのテストをする。
    """
    def test_get_prep_value(self):
        """
        LowerCharField の lower_char_field を使用すると大文字が全て小文字になる。
        """
        # lower_char_field = LowerCharField()
        # self.assertEqual('abc', lower_char_field.get_prep_value('ABc'))

    def test_create_notification(self):
        pass
