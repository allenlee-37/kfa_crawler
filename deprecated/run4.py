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

# Headless로 실행
print('Chrome option 설정')
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_experimental_option("detach", True)
# options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

'''메인 페이지로 넘어감'''
url = 'https://www.joinkfa.com/'
driver.get(url)
driver.implicitly_wait(5)
print('메인 페이지 연결')
    
'''팀 검색 페이지로 넘어감'''
print('팀 검색 버튼 클릭')
validator = 0
while validator < 60:
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser01_WebBrowser')
        validator = 100
    except: 
        time.sleep(2)
        validator += 1
search_team = driver.find_element(By.XPATH, '//*[@id="mainMenu3"]/article[3]/div/div[2]/h3/a')
search_team.send_keys(Keys.ENTER)        
print('팀 페이지 연결')

validator = 0
while validator < 60:
    # //*[@id="loading"]
    try:
        element = driver.find_element(By.XPATH, '//*[@id="loading"]')
        display_prop = element.value_of_css_property('display')
        if display_prop == None: validator = 100
        else: raise Exception
    except: 
        time.sleep(2)
        validator +=1
driver.implicitly_wait(5)
time.sleep(5)

print('드랍 다운 옵션 클릭')
driver.find_element(By.XPATH, "//*[@id='selSearchType']/option[text()='축구']").click()
driver.find_element(By.XPATH, "//*[@id='selSearchMasTitl']/option[text()='동호인축구일반']").click()
driver.implicitly_wait(5)

validator = 0
while validator < 60:
    # //*[@id="loading"]
    try:
        element = driver.find_element(By.XPATH, '//*[@id="loading"]')
        display_prop = element.value_of_css_property('display')
        if display_prop == None: validator = 100
        else: raise Exception
    except: 
        time.sleep(2)
        validator +=1
driver.implicitly_wait(5)
time.sleep(5)

elements = driver.find_elements(By.XPATH, '//h4[@class="card-title"]')
driver.implicitly_wait(5)
teams_in_page = [elem.text for elem in elements]
print(teams_in_page)

# page button 누르기
page_button = driver.find_element(By.XPATH, f'/html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[3]')
driver.implicitly_wait(5)
page_button.click()