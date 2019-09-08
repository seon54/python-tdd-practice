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
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, 'lists/.+')
        self.check_for_row_in_list_table('1: 공작깃털 사기')
        time.sleep(10)

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
        # 다시 '공작깃털을 이용해서 그물 만들기' 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 갱신되고 두 개의 아이템이 목록에 보인다.
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 새로운 사용자인 프란시스가 사이트 접속

        # 새로운 브라우저 세션을 이용해 에디스의 정보가 쿠키를 통해 유입되는 것 방지
        self.browser.quit()
        self.browser = webdriver.Chrome(executable_path='../chromedriver.exe')

        # 프란시스가 홈페이지에 접속
        # 에디스의 리스트는 보이지 않음
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('공잣깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # 프란시스가 새로운 작업 아이템을 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL 취득
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 프란시스가 입력한 흔적이 없다는 것 다시 확인
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

        self.fail('Finish the test!')
