# -*- coding: utf-8 -*- 
 
import  time
from pymongo import MongoClient
from mail import Mail
import ConfigParser,os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class alarm_system(object):

    def __init__(self):
	client = MongoClient("10.3.2.113",7017)
	self.db = client.pinpoint
    
    #条件比较
    def alarm(self):
        rules_ret = self.db['alarm_rule'].find({},{'_id':0})
        for rule in rules_ret: 
    	    for r in rule:
    	        #核心
    	        #报警规则开始检测，判断
    	        if r == "rule_list":
    		    data = rule[r]
    		    monitor_data = self.get_data(rule['allow_app'] + '_' + data[0], int(data[1]))
		    mails = rule['rule_email']
		    content = rule['rule_tpl']
		    allow_app = rule['allow_app']
		    app_type = data[0] 

		    if data[3] == ">":
    	                if int(monitor_data) > int(data[-1]):
			    self.send_alarm(mails, content, allow_app, monitor_data, app_type)
		    if data[3] == "<":
    	                if int(monitor_data) < int(data[-1]):
			    self.send_alarm(mails, content, allow_app, monitor_data, app_type)
		    if data[3] == "=":
    	                if int(monitor_data) ==  int(data[-1]):
			    self.send_alarm(mails, content, allow_app, monitor_data, app_type)


    def send_alarm(self, mails, content, allow_app, monitor_data, app_type):
    	#开始发送邮件进行报警
    	#报警接收人为列表
    	if not mails.endswith(";"):   mails = mails + ";"
    	alarm_peoples = mails.split(";") 
    	alarm_peoples = [i for i in alarm_peoples if i]
    	#处理报警内容模板
    	content = content.encode("utf8") 
    	#模板中的变量的处理
        if '${APP}' in content:
    	    content = content.replace('${APP}', allow_app)
        if '${VALUE}' in content:
    	    content = content.replace('${VALUE}', str(monitor_data))
    		      
        content = content.replace('\n', '</br>')
        content = '<h2>' + content + '</h2>'
    
        #报警标题
        title = '项目:' + allow_app  + '类型'+ app_type 
    
        #发送报警
        self.send_mail(title, alarm_peoples , content)
    	
    
    
    
    
    def get_data(self,server_name,Num ):
        server_name =server_name.lower()
  
        #定义一个时间和查询语句对应的映射关系

        if Num == 1000:     date_expression = {"range_time":{"$lt":1000}}
        if Num == 2000:     date_expression = {"range_time":{"$gt":1000,"$lt":2000}}
        if Num == 3000:     date_expression = {"range_time":{"$gt":2000,"$lt":3000}}
        if Num == 3001:     date_expression = {"range_time":{"$gt":3000}}

        #查找5分钟以前大于3s的数据做统计
        mins = 300         #数据间隔单位s, 默认为5分钟
        Start_Time = int((time.time() -  mins )* 1000)
        endtime = int(time.time() * 1000)
   
        mgo_s3 = self.db[server_name].find({"$and":[ {"startTime":{"$gt" : Start_Time, "$lt" : endtime }} , date_expression ]}).count()
        return mgo_s3 
    
    def send_mail(self, title, tolist, content):
        cf = ConfigParser.ConfigParser()
        filename = os.getcwd() + '/conf/mail.conf'
        cf.read(filename)
    
        smtpserver = cf.get("smtp", "smtpserver")
        smtpaccount = cf.get("smtp", "smtpaccount")
        smtppwd = cf.get("smtp", "smtppwd")
    
        subject = title + 'APM报警邮件'
        mail = Mail(smtpserver , smtpaccount , smtppwd)
        mail.send(subject, content, tolist)
        mail = Mail('127.0.0.1' , '' , '')
        mail.send(subject, content, tolist)
    

def run():
    do = alarm_system()
    alarm = do.alarm()
