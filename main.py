import os

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import emailModule
import exceptionDetect

os.environ["webdriver.chrome.driver"] = '/usr/bin/chromedriver'
option = webdriver.ChromeOptions()
option.add_argument('--headless')   # 无头模式：不提供浏览器的可视化页面，在服务器上跑的时候要把他加上，测试的时候注掉
option.add_argument('--incognito')  # 启用无痕模式
pref = {"profile.default_content_setting_values.geolocation": 2}
option.add_experimental_option("prefs", pref)  # 禁用地理位置
# GitHub服务器需要用这个driver
serv = Service('/usr/bin/chromedriver')
# win上用这个服务器
# serv = Service('./chromedriver.exe')

account = os.environ.get('ACCOUNT').split(';')  # 字符串预处理
user = os.environ.get('USER')
psw = os.environ.get('PSW')
msg = []
browser = webdriver.Chrome(options=option,service=serv) #打开浏览器
for acc in account:
    result = 'Success'
    usr = acc.split(',')
    browser.get('https://sso.ecust.edu.cn/authserver/login?service=https%3A%2F%2Fworkflow.ecust.edu.cn%2Fdefault%2Fwork%2Fuust%2Fzxxsmryb%2Fmrybcn.jsp')  # 进入登陆界面
    browser.find_element(By.ID,'username').send_keys(usr[0])
    browser.find_element(By.ID,'password').send_keys(usr[1])
    browser.find_element(By.TAG_NAME,'button').submit()
    browser.implicitly_wait(1)

    # 判断是否密码错误
    warn = exceptionDetect.isCorrectLogin(browser, msg, usr[0])
    if warn == False:
        # 登录成功
        browser.find_element(By.CSS_SELECTOR,'.iCheck-helper').click()
        browser.find_element(By.ID,'post').click()
        browser.implicitly_wait(1)

        #判断是否已经填报
        warn = exceptionDetect.isFinished(browser, msg, usr[0])
        if warn == False:
            # 还未填报
            # 每日健康报送
            browser.find_element(By.ID, 'radio_swjkzk20').click()        # radio_swjkzk20 健康
            browser.find_element(By.ID, 'radio_xrywz32').click()         # radio_xrywz32 徐汇校区
            browser.find_element(By.ID, 'radio_xcm5').click()           # 行程吗绿色确定
            browser.find_element(By.ID, 'radio_twsfzc9').click()           # 体温正常（默认已填）
            browser.find_element(By.ID, 'radio_jkmsflm13').click()         # 健康发绿色确定（默认已填）
            browser.find_element(By.ID, 'radio_sfycxxwc44').click()        # 没有从学校外出
            browser.find_element(By.ID, 'post').click()                    # 提交表单
            browser.implicitly_wait(1)

            #确认界面
            browser.find_element(By.LINK_TEXT, '确定').click()
            browser.find_element(By.LINK_TEXT, '确定').click()
            element = [usr[0],result]
            msg.append(element)
#判断是否成功提交

browser.close()

emailModule.sendMail(mail_user=user, mail_pass=psw, messageCode=msg)