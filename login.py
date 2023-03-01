# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By

from constant import *


class Login:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        # 注册驱动
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)

    def login(self):
        # 登录网站
        self.driver.get(self.url)

        # 获取登录框
        elem = self.driver.find_element(By.XPATH, XPATH_LOGIN_LABEL)
        elem.click()

        # 获取用户名框，输入前清空
        elem = self.driver.find_element(By.XPATH, XPATH_LOGIN_USERNAME_INPUT)
        elem.clear()
        elem.send_keys(self.username)

        # 获取密码框对象, 清空后输入密码
        elem = self.driver.find_element(By.XPATH, XPATH_LOGIN_PASSWORD_INPUT)
        elem.clear()
        elem.send_keys(self.password)

        # 获取登录按钮，点击登录
        elem = self.driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON)
        elem.click()
