import re
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string
from django.urls import resolve
from .views import home_page


def remove_csrf_tag(text):
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'
        response = home_page(request)
        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = render_to_string('home.html', {'new_item_text': '신규 작업 아이템'})
        self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))
        # self.assertEqual(response.content.decode(), expected_html)
