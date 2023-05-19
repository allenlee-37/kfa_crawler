import argparse
import os

from selenium.webdriver.common.by import By
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


import pandas as pd
from tqdm import tqdm

from datetime import datetime
import re

import time

from bs4 import BeautifulSoup

'''Headless로 실행'''
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_experimental_option("detach", True)
options.add_argument('headless')
options.add_argument('disable-gpu')
print('Chrome option 설정')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = 'https://www.joinkfa.com/'

'''드라이버 url 연결'''
driver.get(url)
driver.implicitly_wait(50)
time.sleep(20)
print('url 연결')

'''iframe 연결'''
driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser01_WebBrowser')
driver.implicitly_wait(10)

'''팀 페이지 도달'''
search_team = driver.find_element(By.XPATH, '//*[@id="mainMenu3"]/article[3]/div/div[2]/h3/a')
search_team.send_keys(Keys.ENTER)
driver.implicitly_wait(60)
time.sleep(10)
print('팀 페이지 연결')

'''드랍 다운 옵션 선택'''
driver.switch_to.default_content()
driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')

driver.find_element(By.XPATH, "//*[@id='selSearchType']/option[text()='축구']").click()
driver.implicitly_wait(10)
driver.find_element(By.XPATH, "//*[@id='selSearchMasTitl']/option[text()='동호인축구일반']").click()
driver.implicitly_wait(10)
time.sleep(30)
print('드랍 다운 옵션 선택 완')

'''프레임 조정'''
driver.switch_to.default_content()
driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
driver.implicitly_wait(60)
time.sleep(20)
print('프레임 조정')

team_names = driver.find_elements(By.XPATH, '//*[@id="teamBlogList1"]/div[2]/div/div/div/div[2]/h4')
for team_name in team_names:
    print(team_name.txt)

# //*[@id="teamBlogList1"]/div[2]/div/div/div/div[2]/h4
#/html/body/div[3]/section/div/div[3]/div[1]/div[1]/div/div/div/div[2]/h4

driver.quit()