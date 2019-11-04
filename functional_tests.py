import os
from selenium import webdriver

path = os.path.join(os.getcwd() + '/..', 'geckodriver')
browser = webdriver.Firefox(executable_path=path)
browser.get('http://localhost:8000')

assert 'Django' in browser.title
