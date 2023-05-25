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
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def validation_loading():
    
    print(f'로딩이 없어지길 기다립니다 - {datetime.now()}')
    validator = 0
    while validator < 60:
        # //*[@id="loading"]
        try:
            element = driver.find_element(By.XPATH, '//*[@id="loading"]')
            display_prop = element.value_of_css_property('display')
            if display_prop == 'none': validator = 100
            else: raise Exception
        except: 
            time.sleep(2)
            validator +=1
    time.sleep(5)
    print(f'로딩이 없음 - {datetime.now()}')

def validation_frame():
    
    print(f'프레임 나타나길 기다립니다. - {datetime.now()}')
    validator = 0
    while validator < 60:
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
            validator = 100
            print(f'프레임 있음 - {datetime.now()}')
        except:
            time.sleep(2)
            validator += 1
            print(f'프레임이 없네? - {datetime.now()}')
    time.sleep(3)
    
def open_main_site():
    driver.implicitly_wait(3)
    '''메인 페이지로 넘어감'''
    url = 'https://www.joinkfa.com/'
    driver.get(url)
    print('메인 페이지 연결')
    
def open_team_page():
    driver.implicitly_wait(3)
    '''팀 검색 페이지로 넘어감'''
    print('팀 검색 버튼 클릭')
    validator = 0
    while validator < 60:
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser01_WebBrowser')
            search_team = driver.find_element(By.XPATH, '//*[@id="mainMenu3"]/article[3]/div/div[2]/h3/a')
            validator = 100
        except: 
            time.sleep(2)
            validator += 1
    search_team.send_keys(Keys.ENTER)        
    print('>>>>>>>>> 팀 페이지 연결 >>>>>>>>>')
    
def drop_down_option(dropdown1, dropdown2):
    print('>>>>>>>>> 드랍 다운 옵션 클릭 >>>>>>>>>')
    driver.find_element(By.XPATH, f"//*[@id='selSearchType']/option[text()='{dropdown1}']").click()
    driver.find_element(By.XPATH, f"//*[@id='selSearchMasTitl']/option[text()='{dropdown2}']").click()
    validation_loading()
    return driver

def crawl_page_team_name():
    validator = 0
    while validator < 70:
        try:
            elements = driver.find_elements(By.XPATH, '//h4[@class="card-title"]')
            result = [elem.text for elem in elements]
            if len(result) < 1: raise Exception
            else: validator = 100
        except: 
            time.sleep(2)
            validator += 1
            if validator == 60:
                driver.quit()
                break
    return result

def choose_page(page_num):
    if page_num%10==0:
        button_number = 11
    else:
        button_number = page_num%10+1 # 3번을 누르고 싶다면 4가 된다.

    validator = 0
    while validator < 70:
        try:
            page_button = driver.find_element(By.XPATH, f'/html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[{button_number}]/a')
            if int(page_button.text) == page_num: 
                page_button.send_keys(Keys.ENTER)    
                print(f'{page_num}-{page_button.text} 페이지 클릭이 됐다!')
                validator = 100
            else: raise Exception
        except: 
            print('버튼 클릭이 안되나?')
            validator +=1
            time.sleep(5)
            if validator == 60:
                driver.quit()
                break
            else: pass

def next_page_button():
    validator = 0
    while validator < 70:
        try: 
            next_page = driver.find_element(By.XPATH, '/html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[12]/a')
            next_page.send_keys(Keys.ENTER) 
            validator = 100
            print(f'다음 페이지 버튼이 눌러졌다!')
            what_decimal = driver.find_element(By.XPATH, f'/html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[2]/a')
            print(f'{int(what_decimal.text)+10} 페이지까지 왔다.')
        except:
            print(f'버튼이 안 눌러진다... - {datetime.now()}')
            time.sleep(5)
            validator += 1
            if validator == 60: 
                driver.quit()
                break

def crawl_iteration(start, end, result_path):
    driver.implicitly_wait(3)
    '''시작 페이지로 이동'''
    for i in range((start-1)//10): 
        next_page_button()
        validation_loading()
        time.sleep(2)
    
    validation_loading()

    if start%10==1: pass
    else: choose_page(start)

    validation_loading()
    time.sleep(2)

    teams = []
    teams.extend(crawl_page_team_name())
    result = pd.DataFrame({'팀명': teams,
                           '페이지': start})
    print(f'{start} 페이지 수집 완료')

    '''이후 반복적으로 수집'''
    for page_num in tqdm(range(start+1, end)):
        print(f'{page_num} 페이지 작업 시작 - {datetime.now()}')
        if (page_num)%10==1: next_page_button()
        else: choose_page(page_num)
        validation_loading()
        time.sleep(1)

        new_teams = crawl_page_team_name()
        new_row = pd.DataFrame({'팀명': new_teams,
                                '페이지': page_num})
        result = pd.concat([result, new_row])

        file_name = f'result_path/{start}-{end}-{page_num}-팀명'
        result.to_csv(f'{file_name}.csv')
        print(f'>>>>>>>>> {file_name}.csv 저장되었음 >>>>>>>>>')

def main():
    try:
        print(f'작업 시작 - {datetime.now()}')
        open_main_site()
        
        open_team_page()
        validation_frame()
        validation_loading()
        
        drop_down_option(dropdown1 = '축구', dropdown2 = '초등')
        validation_frame()
        validation_loading()
        
        result_folder = 'result/초등'
        crawl_iteration(start=0, end=66, result_path=result_folder)
        
        driver.quit()
    except: 
        driver.quit()

if __name__ == "__main__": 
    main()