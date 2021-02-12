from django.test import TestCase
from django.core.urlresolvers import resolve
from clans.views import home



class ClanUrlTests(TestCase):

    def test_url_resolves_to_home_view(self):
        found = resolve('')
        self.assertEqual(found.func, home)

    def test_url_resolves_to_user_invite_notice_view(self):
        found = resolve('')

