import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import base64

# 检测是否需要输入验证码
def isVerification(browser):
    errorMessages = browser.find_elements(By.CLASS_NAME, 'auth_error')
    for Mes in errorMessages:
        if Mes.text == '请输入验证码':
            return True
    return False

# 检测是否出现用户名或密码错误
def isAccountExcetpion(browser):
    errorMessages = browser.find_elements(By.CLASS_NAME, 'auth_error')
    for Mes in errorMessages:
        if Mes.text == '您提供的用户名或者密码有误':
            return True
    return False

# 检测是否出现登录错误
def isCorrectLogin(browser,msg, usr):
    errTime = 0
    correctCode = False
    while errTime <= 2 and correctCode == False:
        veriFlag = isVerification()
        accountFlag = isAccountExcetpion()
        if accountFlag == True:
            print("密码错误，执行退出程序")
            msg.append([usr,"密码错误，执行退出程序"])
            return True
        if veriFlag == True:
            # 输入验证码
            img = browser.find_element(By.ID, "captchaImg")
            data = img.screenshot_as_png
            base64_data = base64.b64encode(data)
            access_token = '24.83828a5a12deaf15f3b5dc5bd4aae11f.2592000.1667633689.282335-27774282'
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
            params = {"image": base64_data}
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            content = response.json()
            words = content['words_result'][0]['words'].replace(' ', '')
            browser.find_element(By.ID, 'captchaResponse').send_keys(words)
            browser.find_element(By.TAG_NAME, 'button').submit()
            errTime += 1
        else:
            correctCode = True

    if errTime >= 2:
        print("登录验证码输错次数太多，退出程序")
        msg.append([usr, "登录验证码输错次数太多，退出程序"])
        return True

    # 登录成功部分
    print("登录成功")
    return False

# 判断是否已经填报过了
def isFinished(browser, msg, usr):
    message = browser.find_elements(By.ID,'layui-layer100001')
    if len(message) == 0:
        return False
    msg.append([usr,'今天已经填报过了'])
    return True

