# -*- coding: utf-8 -*- 

from base import *
import json



class AppRulesAdd_Handler(BaseHandler):

    def post(self,*args, **kwargs):
        ret = json.loads(self.request.body)
	try:
	    self.db.api_interface_rules.insert_one(ret)
	    self.write({'status':'ok','msg':'接口规则添加成功!!'})
	except:
	    self.db.api_interface_rules.find_one_and_delete({'_id': ret['_id']})
	    self.db.api_interface_rules.insert_one(ret)
	    self.write({'status':'error','msg':'这个APP已经更新!!'})

class AppRulesApply_Handler(BaseHandler):

    def post(self,*args, **kwargs):
	request_dict = self.request.arguments
	_id = request_dict['_id'][0]
	ret = self.db.api_interface_rules.find_one({'_id':_id})
	if ret:
	    self.write({'status':'ok','msg':ret})
	else:
	    self.write({'status':'error','msg':'记录不存在!!'})
