import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time

def get_table():
    req_url = 'https://leetcode.com/tag/array/'
    driver = webdriver.Firefox()
    lc_login(driver)
    driver.get(req_url)
    #time for javascript to load
    time.sleep(20)
    soup = BeautifulSoup(driver.page_source, 'lxml') # Parse the HTML as a string
    table = soup.find_all('table')[0]
    print(table)

def lc_login(driver):
   post_url = 'https://leetcode.com/accounts/login/'
   driver.get(post_url)
   #time for javascript to load
   time.sleep(6)

   username = driver.find_element_by_id("id_login")
   username.clear()
   username.send_keys("i.m.ralk@gmail.com")
   time.sleep(2.2)

   password = driver.find_element_by_id("id_password")
   password.clear()
   password.send_keys(os.environ["my_env_var"])
   time.sleep(1.4)

   driver.find_element_by_id("signin_btn").click()