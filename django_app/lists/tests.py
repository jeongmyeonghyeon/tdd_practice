import re

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import resolve
from django.test import TestCase
from .views import home_page


class HomePageTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(
            re.sub(self.pattern_input_csrf, '', response.content.decode()),
            re.sub(self.pattern_input_csrf, '', expected_html)
        )

    def test_home_page_can_save_a_POST_request(self):
        # 설정(Setup)
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        # 처리(Exercise)
        response = home_page(request)

        # 어설션(assert)
        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': '신규 작업 아이템'}
        )
        self.assertEqual(response.content.decode(), expected_html)
