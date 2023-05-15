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
url = 'https://www.joinkfa.com/'

print('url 연결')
driver.get(url)
driver.implicitly_wait(50)
time.sleep(5)

# iframe으로 넘어가야함
driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser01_WebBrowser')
driver.implicitly_wait(10)
# 팀 검색
search_team = driver.find_element(By.XPATH, '//*[@id="mainMenu3"]/article[3]/div/div[2]/h3/a')
driver.implicitly_wait(10)
time.sleep(5)

print('팀 페이지 연결')
search_team.send_keys(Keys.ENTER)

driver.implicitly_wait(10)
time.sleep(5)

# 반복문 1~10까지
# 카드 클릭 > 안의 페이지 내용 긁어오기
team_names = []
team_infos = []
for card_num in range(1, 11):
    # 프레임 조정 
    driver.switch_to.default_content()
    driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
    driver.implicitly_wait(10)

    # 드롭 다운 '축구' 선택
    # 드롭 다운 '동호인 축구 일반' 선택
    driver.find_element(By.XPATH, "//*[@id='selSearchType']/option[text()='축구']").click()
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[@id='selSearchMasTitl']/option[text()='동호인축구일반']").click()
    driver.implicitly_wait(10)
    
    # 로딩 기다리기
    time.sleep(15)
    # 프레임 조정
    driver.switch_to.default_content()
    driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
    time.sleep(1)
    driver.implicitly_wait(10)

    # 팀 카드 클릭
    driver.find_element(By.XPATH, f'//*[@id="teamBlogList1"]/div[{card_num}]').click()
    time.sleep(1)
    driver.implicitly_wait(10)

    driver.switch_to.default_content()
    time.sleep(1)
    driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
    
    time.sleep(5)
    team_name = driver.find_element(By.XPATH, '//*[@id="hTeamName"]').text
    card_back = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div').text

    team_names.append(team_name)
    team_infos.append(card_back)
    print(f'1페이지 카드 번호: {card_num}')
    driver.back()

page1 = pd.DataFrame({'팀명': team_names,
              '정보': team_infos})

page1.to_csv('test_result.csv')

for page_num in tqdm(range(2, 100)):
    for card_num in range(1,11):
            
        # 프레임 조정 하고
        driver.switch_to.default_content()
        driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
        driver.implicitly_wait(10)

        driver.find_element(By.XPATH, "//*[@id='selSearchType']/option[text()='축구']").click()
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, "//*[@id='selSearchMasTitl']/option[text()='동호인축구일반']").click()
        driver.implicitly_wait(10)

        '''10 이상일 때는 계속해서 페이지를 올려가야함'''
        if page_num>10:
            # 다음 버튼 누르기
            # 10의 배수 만큼 반복해서 눌러야함
            # //*[@id="page_DisAgent"]/li[12]/a
            for i in range(page_num//10):
                driver.find_element(By.XPATH, '//*[@id="page_DisAgent"]/li[12]/a').click()
                driver.implicitly_wait(10)
                time.sleep(10)
            # //*[@id="page_DisAgent"]/li[2]/a
        else: pass
        # page_num+1의 페이지 번호 누르기
        # 10을 넘어가면 다음 페이지 버튼을 누르도록 if문 추가해야함
        if page_num%10 == 0:
            button_number = 10
        else: button_number = page_num%10+1
        
        driver.implicitly_wait(10)
        time.sleep(10)
        
        driver.find_element(By.XPATH, f'//*[@id="page_DisAgent"]/li[{button_number}]/a').click()


        try:
            driver.implicitly_wait(10)
            time.sleep(10)
            # 프레임 조정
            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
            driver.implicitly_wait(10)

            # 팀 카드 클릭
            driver.find_element(By.XPATH, f'//*[@id="teamBlogList1"]/div[{card_num}]').click()
            driver.implicitly_wait(10)

            driver.switch_to.default_content()
            driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
            driver.implicitly_wait(10)

            time.sleep(5)
            team_name = driver.find_element(By.XPATH, '//*[@id="hTeamName"]').text
            card_back = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div').text

            page1 = pd.concat([page1, pd.DataFrame({'팀명': [team_name],'정보': [card_back]})])
            page1.to_excel(f'./result/backup-data/back-up{card_num//2}.xlsx')
            print(f'{page_num} 페이지의 카드 번호: {card_num}, 열 갯수: {len(page1)}')
            driver.back()
        except: print(f'error in 페이지 {page_num}번, 카드 {card_num}번')
        finally: pass

page1.to_excel(f'./result/final-result.xlsx')