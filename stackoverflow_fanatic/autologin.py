#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

loginUrl = 'https://stackoverflow.com/users/login?ssrc=head&returnurl=http%3a%2f%2fstackoverflow.com%2f'
username = 'iwillnotpostithere'
password = 'noachance'

   
driver = webdriver.Firefox()
driver.get(loginUrl)
assert "Stack Overflow" in driver.title

emailInput = driver.find_element_by_name("email")
passwordInput = driver.find_element_by_name("password")

emailInput.send_keys(username)
passwordInput.send_keys(password)

passwordInput.send_keys(Keys.RETURN)

# wait until logo appear
logo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "hlogo")))

assert driver.current_url == 'http://stackoverflow.com/'
print 'login success'

driver.close()
