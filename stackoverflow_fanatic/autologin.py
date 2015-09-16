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

FFdriver = webdriver.Firefox()
FFdriver.get(loginUrl)
# should be "Log in - Stack Exchange - Stack Overflow"
assert "Stack Overflow" in FFdriver.title

emailInput = FFdriver.find_element_by_name("email")
passwordInput = FFdriver.find_element_by_name("password")

emailInput.send_keys(username)
passwordInput.send_keys(password)

passwordInput.send_keys(Keys.RETURN)

# wait until logo 'stackoverflow' appear
logo = WebDriverWait(FFdriver, 10).until(EC.presence_of_element_located((By.ID, "hlogo")))

# if successfully login, should be redirected to http://stackoverflow.com/
assert FFdriver.current_url == 'http://stackoverflow.com/'
print 'login success'

# not sure if pure login counts or need page reload, check user page 'last seen'
# there's a delay between login and it refresh, just to ensure the page reload once after login in
FFdriver.find_element_by_id('hlogo').click()
# wait for reloading page..
FFdriver.implicitly_wait(10)

FFdriver.close()
