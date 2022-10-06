from smtplib import SMTP_SSL
from email.mime.text import MIMEText

def sendMail(mail_user, mail_pass, messageCode):

    # mail_user="****@qq.com"    #用户名
    # mail_pass="******"   #口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    # mail_message="a text email from python"
    # 接收邮件，设置为你的QQ邮箱

    mail_host = "smtp.qq.com"  # 设置服务器，只能是QQ邮箱
    #MIMEText(text, subType, 'utf-8') 封装发送的信息
    #subType: plain = 发送纯文本信息； html = 发送网页信息
    # utf-8 = 编码格式
    message = MIMEText(messageProcess(messageCode),'plain','utf-8')
    #设置邮件主题
    message["Subject"] = '打卡邮件信息'
    #设置发件人
    message["from"] = mail_user

    #资源调用，打开SMTP_SSL
    with SMTP_SSL(host=mail_host,port=465) as smtp:
        #登录发送邮件的服务器
        smtp.login(user=mail_user,password=mail_pass)
        #实际发送、接收邮件的配置
        smtp.sendmail(from_addr=mail_user, to_addrs=mail_user, msg=message.as_string())

def messageProcess(messageCode):
    listed = []
    if len(messageCode) == 0:
        return '出现 messageCode 为空的错误'
    else:
        for element in messageCode:
            elemented = ':'.join(element)
            listed.append(elemented)
    return '\n'.join(listed)