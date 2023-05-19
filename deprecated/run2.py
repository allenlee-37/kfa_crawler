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

def open_main_site():
    '''메인 페이지로 넘어감'''
    url = 'https://www.joinkfa.com/'
    driver.get(url)
    print('메인 페이지 연결')
    

def open_team_page():
    '''팀 검색 페이지로 넘어감'''
    driver.switch_to.default_content()
    driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser01_WebBrowser')
    # 팀 검색
    print('팀 검색 버튼 클릭')
    search_team = driver.find_element(By.XPATH, '//*[@id="mainMenu3"]/article[3]/div/div[2]/h3/a')
    search_team.send_keys(Keys.ENTER)
    print('팀 페이지 연결')

def drop_down_option():
    # 프레임 조정 
    driver.switch_to.default_content()
    driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
    driver.find_element(By.XPATH, "//*[@id='selSearchType']/option[text()='축구']").click()
    driver.find_element(By.XPATH, "//*[@id='selSearchMasTitl']/option[text()='동호인축구일반']").click()
    print('드랍다운 옵션 클릭')

def crawl_page_team_name():
    driver.switch_to.default_content()
    driver.switch_to.frame('mainframe.VFrameSet.WorkFrame.form.div_work.form.WebBrowser00_WebBrowser')
    elements = driver.find_elements(By.XPATH, '//h4[@class="card-title"]')
    return [elem.text for elem in elements]

def choose_page(page_num):
    button_number = page_num%10+1
    driver.implicitly_wait(30)
    # /html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[6]
    page_button = driver.find_element(By.XPATH, f'/html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[{button_number}]')

    validator = 0
    while validator < 20 :
        if page_button.text == button_number: 
            validator = 100
            page_button.click()
        else:
            time.sleep(5)
            validator += 1
    
    '''if page_button.text == button_number: 
        print(page_button.text)
        page_button.click()
    else:
        time.sleep(30)
        page_button.click()'''

def next_page_button(page_num):
    iteration_number = (page_num-1)//10
    for iteration in range(iteration_number):
        driver.find_element(By.XPATH, '/html/body/div[3]/section/div/div[3]/div[2]/div/ul/li[12]').click()
        
def crawl_iteration(start=2, end=5000):
    teams = []
    teams.extend(crawl_page_team_name())
    print('1페이지 팀명 수집 완료') 

    for page_num in range(start, end):
        print(f'{page_num} 페이지 작업 시작 - {datetime.now()}')
        if page_num < 11: 
            '''1페이지~10페이지까지의 경우들'''
            try:
                print(f'{page_num} 페이지 클릭 시도')
                time.sleep(5)
                choose_page(page_num)
            except:
                print(f'실패 및 재시도')
                time.sleep(30)
                choose_page(page_num)
            finally:
                driver.implicitly_wait(60)
                time.sleep(15)
                new_teams = crawl_page_team_name()
                if len(new_teams) > 15: print(f'성공')
                teams.extend(new_teams)
                
        else:
            try:
                if (page_num-1)%10==0:
                    try:
                        print(f'{page_num} 페이지 다음 페이지 클릭 시도')
                        time.sleep(10)
                        next_page_button(page_num)
                    except:
                        print(f'실패 및 재시도')
                        time.sleep(20)
                        next_page_button(page_num)
                    finally: 
                        driver.implicitly_wait(60)
                        time.sleep(15)
                else:
                    try:
                        print(f'{page_num} 페이지 클릭 시도')
                        time.sleep(10)
                        choose_page(page_num)
                    except:
                        print(f'실패 및 재시도')
                        time.sleep(30)
                        choose_page(page_num)
                    finally: 
                        driver.implicitly_wait(60)
                        time.sleep(15)
                new_teams = crawl_page_team_name()
                if len(new_teams) > 15: print(f'성공')
                teams.extend(new_teams)
                    
                
            except:
                print(f'{page_num} 페이지 실패')
                driver.quit()

        team_name = pd.DataFrame({'팀명': teams})
        file_name = f'{start}-{page_num}-팀명'
        team_name.to_csv(f'./result/팀명/{file_name}.csv')
        print(f'{file_name}.csv 저장되었음')


def main():
    print(f'작업 시작 - {datetime.now()}')
    open_main_site()
    time.sleep(40)
    driver.implicitly_wait(60)
    print('메인 페이지 연결 완료')

    open_team_page()
    time.sleep(30)
    driver.implicitly_wait(60)

    drop_down_option()
    time.sleep(30)
    driver.implicitly_wait(60)
    
    start = 2
    end = 500
    crawl_iteration(start, end)

    '''
    teams = []
    teams.extend(crawl_page_team_name())
    print('1페이지 팀명 수집 완료')    

    for page_num in range(1, 5000):
        if page_num < 11: 
            choose_page(page_num)
            teams.extend(crawl_page_team_name())
            print(f'페이지 팀명 수집 완료: {page_num} 페이지')

            team_name = pd.DataFrame({'팀명': teams})
            team_name.to_csv('./result/팀명/팀명.csv')
        else:
            if (page_num-1)%10==0:
                next_page_button(page_num)
                teams.extend(crawl_page_team_name())
                print(f'페이지 팀명 수집 완료: {page_num} 페이지')

                team_name = pd.DataFrame({'팀명': teams})
                team_name.to_csv('./result/팀명/팀명.csv')
            else:
                choose_page(page_num)
                teams.extend(crawl_page_team_name())
                print(f'페이지 팀명 수집 완료: {page_num} 페이지')
                
                team_name = pd.DataFrame({'팀명': teams})
                team_name.to_csv('./result/팀명/팀명.csv')'''
    driver.quit()
        
        
    

    

if __name__ == "__main__": 
    main()