# -*- coding: utf-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ConfigParser,os
 
 
class Mail:
 
    def __init__(self, smtp, user, pwd):
        self.smtp = smtp
        self.user = user
        self.pwd = pwd
        self.isauth = True
 
    def parse_send(self, subject, content, plugin):
        return subject, content, plugin
 
    def send(self, subject, content, tolist, cclist=[], plugins=[]):
        msg = MIMEMultipart()
        msg.set_charset('utf-8')
        msg['from'] = self.user
        msg['to'] = ','.join(tolist)
        if cclist:
            msg['cc'] = ','.join(cclist)
        msg['subject'] = subject
        msg.attach(MIMEText(content, 'html', 'utf-8'))
        for plugin in plugins:
            f = MIMEApplication(plugin['content'])
            f.add_header('content-disposition', 'attachment',
                         filename=plugin['subject'])
            msg.attach(f)
 
        s = smtplib.SMTP(self.smtp)
        s.set_debuglevel(smtplib.SMTP.debuglevel)
        if self.isauth:
            s.docmd("EHLO %s" % self.smtp)
 
        try:
            s.starttls()
        except smtplib.SMTPException, e:
            pass  # smtp 服务器不支持 ssl
 
        try:
            s.login(self.user, self.pwd)
        except smtplib.SMTPException, e:
            pass  # smtp 服务器不需要登陆
 
        r = s.sendmail(self.user, tolist, msg.as_string())
        s.close()
        return r
 
if __name__ == "__main__":
    subject = '发送邮件测试'
    content = '测试'

    mail = Mail('127.0.0.1' , 'root' , '')
    tolist = ['zhongyi.chen@9icaishi.net']
    mail.send(subject, content, tolist)
    print 'mail was sent!'
