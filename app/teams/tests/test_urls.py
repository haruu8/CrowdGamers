from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from teams import views
from django.contrib.auth import get_user_model



class TeamUrlRoutingTests(TestCase):
    """
    正しい view が呼び出されているかテスト

    Notes
    -----
    test_url_resolves_to_*** で関数定義している。 *** は views の名前
    """
    # def setUp(self):
    #     get_user_model().objects.create_user(
    #         username='hoge',
    #     )

    def test_url_resolves_to_home(self):
        found = resolve('')
        self.assertEqual(found.func, views.home)



# class TeamHtmlTests(TestCase):
#     """
#     正しい html が表示されているかテスト
#     """
#     def test_home_html(self):
#         request = HttpRequest()
#         response = views.home(request)
#         expected_html = render_to_string('teams/home.html')
#         self.assertEqual(response.content.decode(), expected_html)
