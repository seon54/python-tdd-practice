from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='../chromedriver.exe')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 웹 사이트 확인
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do' 표시
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 작업 추가
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # '공작깃털 사기' 텍스트 상자 입력
        inputbox.send_keys('공작깃털 사기')

        # 엔터키 누르면 페이지가 갱신되고 작업 목록에 '1: 공작깃털 사기' 아이템 추가
        inputbox.send_keys(Keys.ENTER)
        # self.check_for_row_in_list_table('1: 공작깃털 사기')
        time.sleep(10)

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
        # 다시 '공작깃털을 이용해서 그물 만들기' 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 갱신되고 두 개의 아이템이 목록에 보인다.
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 사이트에서 입력한 목록을 위한 특정 URL과 설명 함께 제공

        self.fail('Finish the test!')


'''
< 1장 >
browser = webdriver.Chrome(executable_path='../chromedriver.exe')

# 웹 사이트 확인
browser.get('http://localhost:8000')

# 웹 페이지 타이틀과 헤더가 'To-Do' 표시
assert 'To-Do' in browser.title, 'Brower title was ' + browser.title

# '공작깃털 사기' 텍스트 상자 입력

# 엔터키 누르면 페이지가 갱신되고 작업 목록에 '1: 공작깃털 사기' 아이템 추가

# 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
# 다시 '공작깃털을 이용해서 그물 만들기' 입력

# 페이지는 다시 갱신되고, 두 개의 아이템이 목록에 보인다
# 사이트에서 입력한 목록을 위한 특정 URL과 설명 함께 지공

# 해당 URL에 접속하면 작업 목록 확인 가능

browser.quit()
'''
