import os
import time
import unittest
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class NewVisitorTest(LiveServerTestCase):
    path = os.path.join(os.path.dirname(os.getcwd()), 'geckodriver')

    def setUp(self) -> None:

        self.browser = webdriver.Firefox(executable_path=self.path)
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고 웹사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do' 표시
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 작업 추가
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # '공작깃털 사기'라고 텍스트 상자에 입력기
        inputbox.send_keys('공작깃털 사기')

        # 엔터키를 치면 페이지가 갱신되고 작업 목록에
        # '1: 공작깃털 사기' 아이템 추가
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table("1: 공작깃털 사기")

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
        # 다시 '공작깃털을 이용해서 그물 만들기' 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보임
        self.check_for_row_in_list_table("1: 공작깃털 사기")
        self.check_for_row_in_list_table("2: 공작깃털을 이용해서 그물 만들기")

        ## 새로운 사용자 프란시스 접속
        ## 새로운 브라우저 세션을 이용해 에디스의 정보가 쿠키를 통해 유입되는 것 방지
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=self.path)

        # 프란시스가 홈페이지에 접속하고 에디스의 리스트는 보이지 않음
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # 프란시스가 새로운 작업 아이템 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 프란시스가 전용 URL 취득
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없는지 확인
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

        # 둘 다 만족하고 잠자리에 든다

