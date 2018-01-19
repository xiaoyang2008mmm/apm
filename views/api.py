# -*- coding: utf-8 -*- 

from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor
import tornado.web
import json
import tornado.gen
from base import *
from dnsip import IP
import os




#接口示例
#http://apm.9liuda.com/api/interface/?apptype=kskp2   

class InterfaceHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,*args, **kwargs):

	ret = json.loads(self.request.body)
        res = yield self.save_mongodb(ret)
	self.write({'status':'OK','msg': 'server already get data!!! '})
        self.finish()

    @run_on_executor
    def save_mongodb(self,ret):
        real_ip = self.request.remote_ip

	#解析IP地址物理位置，获取省份
	IP.load(os.path.abspath("./data/mydata4vipday2.dat"))

	#获取app项目类型
	request_dict = self.request.arguments
	
	apptype = "wuli"   #默认设置为wuli
	if request_dict:
	    #兼容app项目api接口改为uuid的模式
	    try:
	        apptype = request_dict['apptype'][0]
	    except:
	        appid = request_dict['appid'][0]
		apptype = (self.db.appnames.find_one({'_id':appid},{'app_table_name':1,'_id':0}))['app_table_name']

	for key in ret:
	    collection = self.db[apptype + '_' + key]
	    data = ret[key][0]
	    data['range_time'] = int(data['endTime']) - int(data['startTime'])
            data['client_ip'] = real_ip
            data['location_ip'] = IP.find(real_ip) 
	    result = collection.insert_one(data)
	return True


    def get(self,*args, **kwargs):
	raise tornado.web.HTTPError(403)


class GetConfigHandler(BaseHandler):

    def get(self,*args, **kwargs):



	#生成配置，供客户端启动时候调用
	request_dict = self.request.arguments
	if request_dict:
            _id = request_dict['appid'][0]
	    upload_url = '{2}://{0}/api/interface/?appid={1}'.format('apm.9liuda.com' , _id, self.request.protocol)
            ret = self.db.api_interface_rules.find_one({'_id':_id})
            if ret:
	        specialurl_list = [[ret['first_urlname'], ret['first_urlperf'] ]]
	        defaulturl_list = ret['last_value']
		dynamiclists_list = ret['dynamiclists']
		for l in dynamiclists_list:
		    specialurl_list.append([l[0],l[1]])

		data = {'specialurl_list':specialurl_list, 'defaulturl_list':defaulturl_list, 'upload_url':upload_url, 'version':'1.0'}


                self.write({'status':'ok','appapiinfo':data})
            else:
                self.write({'status':'error','msg':'规则记录不存在,清先添加规则!!!'})
	else:
	    raise tornado.web.HTTPError(403)

