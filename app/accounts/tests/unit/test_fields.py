from django.test import TestCase
from accounts.fields import LowerCharField



class TestFields(TestCase):
    """
    カスタムフィールドのテストをする。
    """
    def test_get_prep_value(self):
        """
        LowerCharField の lower_char_field を使用すると大文字が全て小文字になる。
        """
        lower_char_field = LowerCharField()
        self.assertEqual('abc', lower_char_field.get_prep_value('ABc'))
