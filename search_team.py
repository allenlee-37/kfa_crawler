import multiprocessing
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

'''드라이버 옵션'''
# Headless로 실행
print('Chrome option 설정')
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_experimental_option("detach", True)
options.add_argument('headless')
options.add_argument('disable-gpu')

def validation_loading():
    print(f'로딩이 없어지길 기다립니다 - {datetime.now()}')
    validator = 0
    while validator < 30:
        # //*[@id="loading"] 
        try:
            element = driver.find_element(By.XPATH, '//*[@id="loading"]')
            display_prop = element.value_of_css_property('display')
            if display_prop == 'none': validator = 100
            else: raise Exception
        except: 
            time.sleep(2)
            validator +=1
            if validator == 20: driver.quite()
    time.sleep(5)
    print(f'로딩이 없음 - {datetime.now()}')

'''드라이버 실행'''
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

'''홈페이지 연결'''
def open_main_site():
    driver.implicitly_wait(3)
    '''메인 페이지로 넘어감'''
    url = 'https://www.joinkfa.com/'
    driver.get(url)
    driver.implicitly_wait(3)
    print('메인 페이지 연결')

def main_page_validate():
    validator = 0
    while validator < 21:
        try:
            # 검토용
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser01_WebBrowser')
            driver.find_element(By.XPATH, '//*[@id="mainMenu3"]/article[3]/div/div[2]/h3/a')
            validator=100
        except:
            time.sleep(2)
            validator +=1
            if validator ==20: driver.quit()

'''검색 버튼 입력'''
# input: //*[@id="searchKeyword"]
def click_search(team_name):
    driver.implicitly_wait(60)
    time.sleep(1)
    '''팀 검색 페이지로 넘어감'''

    validator = 0
    while validator < 21:
        try:
            # 검색용
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.WebBrowser00_WebBrowser')
            driver.find_element(By.XPATH, '//*[@id="top-search-trigger"]').click()
            validator = 100
        except: 
            time.sleep(2)
            print('.')
            validator += 1
            if validator == 20: driver.quit()

    time.sleep(2)
    
    validator=0
    while validator < 21:
        try:
            driver.find_element(By.XPATH, '//button[@class="btn h-bg-alt"]')
            driver.implicitly_wait(2)
            driver.find_element(By.XPATH, '//input[@id="searchKeyword"]').send_keys(team_name)
            validator = 100
        except:
            time.sleep(2)
            print('.')
            validator += 1
            if validator == 20: driver.quit()
    driver.implicitly_wait(2)
    driver.find_element(By.XPATH, '//button[@class="btn h-bg-alt"]').send_keys(Keys.ENTER)
    print('>>>>>>>>> 팀 페이지 연결 >>>>>>>>>')

    validator=0
    while validator < 21:
        # /html/body/div[2]/section/div/div/div/div/div/div[1]/div[4]/div[1]/div/a/span
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
            time.sleep(1)
            search_result = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div/div/div/div/div[1]/div[4]/div/div/a')
            print(search_result.text)
            validator=100
        except:
            time.sleep(2)
            print(f'try {validator}th time')
            validator += 1
            if validator == 20: driver.quit()
    if team_name == search_result.text: search_result.send_keys(Keys.ENTER)

def team_info(team_name, iteration):
    time.sleep(2)
    driver.implicitly_wait(60)
    validator=0
    while validator < 21:
        # /html/body/div[2]/section/div/div/div/div/div/div[1]/div[4]/div[1]/div/a/span
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
            validator=100
        except:
            time.sleep(2)
            validator += 1
            if validator == 20: driver.quit()
        
    name = [team_name]
    try: date = [driver.find_element(By.XPATH, '//*[@id="teamCreateDate"] ').text]
    except: date = ['확인 x']

    try: address = [driver.find_element(By.XPATH, '//*[@id="teamAddress"]').text]
    except: address = ['확인 x']
    
    try: telephone = [driver.find_element(By.XPATH, '//*[@id="teamContact"]').text]
    except: telephone = ['확인 x']
    
    try: director = [driver.find_element(By.XPATH, '//*[@id="teamCoachName"]').text]
    except: director = ['확인 x']

    df = pd.DataFrame({'iteration': [iteration],
                       '팀명': name,
                       '날짜':date,
                       '주소':address,
                       '연락처':telephone,
                       '감독':director})
    return df
 
def main():
    '''팀명'''
    teams = pd.read_excel('result/input/try3.xlsx')
    team_names = teams['팀명']
    print(f'대상 숫자 {len(team_names)}')
    
    open_main_site()
    main_page_validate()

    click_search(team_names[0])
    row1 = team_info(team_names[0], 0)
  
    start = 0
    end = 57
    print(f'시작: {start}')
    print(f'끝: {end}')
    print(f'대상 수: {end-start}')

    for i in tqdm(range(start, end)):
        click_search(team_names[i])
        row2 = team_info(team_names[i], i)
        row1 = pd.concat([row1, row2])
        row1.to_csv(f'result/output/{start}-{end}-{i}th.csv')
        print(f'result/output/{start}-{end}-{i}th file saved to csv')
    row1.to_csv(f'result/output/{start}-{end}-final.csv')

if __name__ == "__main__": 
    
    start = time.time()
    main()
    end = time.time()

    print(f'수행시간 {start - end}')