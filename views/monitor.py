# -*- coding: utf-8 -*- 
import tornado.web
import MySQLdb ,json
import tornado.gen
from base import *





class AppMonitor_Handler(BaseHandler):

    def get(self,*args, **kwargs):
	rules = self.db.alarm_rule.find({},{'_id':0})
        __dict = {'rules':rules }
        self.render('appmonitor.html', **__dict)

    def post(self,*args, **kwargs):
        ret = json.loads(self.request.body)
	self.db['alarm_rule'].insert_one(ret)
	self.write({'status':'ok','msg':'规则录入成功'})
