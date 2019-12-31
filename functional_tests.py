import os
import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        path = os.path.join(os.path.dirname(os.getcwd()), 'geckodriver')
        self.browser = webdriver.Firefox(executable_path=path)
        self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 에디스는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고 웹사이트를 확인하러 간다.
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: 공작깃털 사기' for row in rows), "신규 작업 작업이 테이블에 표시되지 않는다")

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자 존재
        # 다시 '공작깃털을 이용해서 그물 만들기' 입력
        self.fail('Finish the test!')

        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보임
        # 입력한 목록을 저장하는 URL 생성

        # 해당 URL에 접속하면 작업 목록 확인 가능


if __name__ == '__main__':
    unittest.main(warnings='ignore')
