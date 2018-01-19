# -*- coding: utf-8 -*- 

import tornado.web
import MySQLdb ,json
import time
from base import *
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor
import fenye,re


#给mongodb创建索引
#self.db.interface.create_index([('startTime',DESCENDING),('range_time',DESCENDING) ])  


class getdata_Handler(BaseHandler):
    executor = ThreadPoolExecutor(20)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        request_dict = self.request.arguments

	#获取高级查询中的ULR和客户端IP地址
	try:
	    http_urlinterface = request_dict['http_urlinterface'][0]
	except:
	    http_urlinterface = '' 
	try:
	    client_address = request_dict['client_address'][0]
	except:
	    client_address = '' 
	#拼凑表名
	tab_prefix = request_dict['allow_app'][0]

	serapp_name =  tab_prefix + '_' + (request_dict['server_name'])[0]

	Start_Time = (request_dict['starttime'])[0]

	endtime = (request_dict['endtime'])[0]

	range_hours = int((request_dict['range'])[0])

	#查找range_hours小时以前的数据
	if Start_Time =="":
	    Start_Time = int((time.time() - range_hours * 3600 )* 1000) 
	else:
	    Start_Time = self.datetime_timestamp(Start_Time)
	if endtime == "": 
	    endtime = int(time.time() * 1000) + 300000 
	else:
	    endtime = self.datetime_timestamp(endtime)
	

	time_list = [i for i in range(Start_Time, endtime, 300000)]


	x_data = map(self.timestamp_datetime, time_list)
	
	res = yield self.do_data(serapp_name,Start_Time,endtime,x_data ,http_urlinterface,client_address)
	self.write(res)
        self.finish()
	
    @run_on_executor
    def do_data(self,serapp_name,Start_Time,endtime,x_data,http_urlinterface,client_address):
    	    """mongodb查询
    	    """
	    mgo_1s_list = []
	    mgo_2s_list = []
	    mgo_3s_list = []
	    mgo_4s_list = []

	    #利用mongdb聚合实现各个省份的pv访问和平均耗时计算
	    case_list = [  {"$match":{"startTime":{"$gt" : Start_Time, "$lt" : endtime }}} ,
                           {"$group" : {"_id" : "$location_ip", "value" : {"$avg" : "$range_time"},"sum":{"$sum": 1}}}]
	    if client_address:
                case_advance = {"$match":{"client_ip": client_address}} 
	        case_list.insert(1,case_advance)

	    if http_urlinterface:
                case_advance = {"$match":{'requestUrl':{'$regex' : http_urlinterface}}} 
	        case_list.insert(1,case_advance)


	    map_data = self.db[serapp_name].aggregate(case_list)


	    def exec_search(serapp_name,x,y,rangtime,http_urlinterface,client_address):

	        try:
 	            sss  = [ {'$match': {'startTime': {'$gt': x, '$lt': y}}},
                             {'$match': {'range_time': rangtime}} ,
                             {'$group': {'_id':'client_ip', 'count':{'$sum':1},'total':{'$sum':'client_ip'}}}]
		    if client_address:
                        as1 = {"$match":{"client_ip": client_address}} 
                        sss.insert(1,as1)

                    if http_urlinterface:
			as1 = {"$match":{'requestUrl':{'$regex' : http_urlinterface}}} 
                        sss.insert(1,as1)



	            a = self.db[serapp_name].aggregate(sss)
	            f = a.next()
	            return  f['count']
	    	except:
		    return 0


	    a,b = Start_Time, endtime
	    while a < (b-300000):
                a1=a
           	a+=300000
	   	#聚合查询

	   	#小于1s
	   	range_1 =  {"$lt":1000}
	   	mgo_s1 = exec_search(serapp_name, a1, a, range_1,http_urlinterface,client_address) 
	   	mgo_1s_list.append(mgo_s1)
	   	#1-2s
	   	range_2 =  {"$gt":1000,"$lt":2000}
	   	mgo_s2 = exec_search(serapp_name, a1, a, range_2,http_urlinterface,client_address) 
	   	mgo_2s_list.append(mgo_s2)
	   	#2-3s
	   	range_3 =  {"$gt":2000,"$lt":3000}
	   	mgo_s3 = exec_search(serapp_name, a1, a, range_3,http_urlinterface,client_address) 
	   	mgo_3s_list.append(mgo_s3)
	   	#大于3s2
	   	range_4 =  {"$gt":3000}
	   	mgo_s4 = exec_search(serapp_name, a1, a, range_4,http_urlinterface,client_address) 
	   	mgo_4s_list.append(mgo_s4)
	   	#####



	    mgo_data = [
		{'name': '0-1s', 'data':mgo_1s_list},
		{'name': '1-2s', 'data':mgo_2s_list},
		{'name': '2-3s', 'data':mgo_3s_list},
		{'name': '>3s',	 'data':mgo_4s_list}
	       ]


	    #生成全国图数据
            rets = []
            area_pv = []
            for ret in map_data:
	        k = ret['_id']
	        v = int(ret['value'])
	        t = ret['sum']
                area_pv.append([k,t])
                rets.append({"name": k , "value": v})


	    ret = {'categories': x_data , 'data':mgo_data}

	    return {'status':200,'msg':ret, 'china_data':rets ,'area_pv':area_pv}











class Chartsdetail_Handler(BaseHandler):

    def get(self,*args,**kwargs):

	request_dict = self.request.arguments
	#拼凑表名

	#获取高级查询的参数
	c_ip = request_dict['c_ip'][0]
	requesturl = request_dict['requesturl'][0]
	###
        tab_prefix = request_dict['allow_app'][0]
        page = request_dict['page'][0]
        serapp_name =  tab_prefix + '_' + (request_dict['serverName'])[0]

	startTime = self.datetime_timestamp(request_dict['endTime'][0])
	endTime = startTime + 300000    #5分钟以前	

	Num = int(request_dict['type'][0])

	if 'interface' in serapp_name: 
	    tab_th_list = ['client_ip','location_ip','startTime','endTime' ,'range_time' , 'requestUrl','requestId']
	if 'dns' in serapp_name:
	    tab_th_list = ['client_ip','location_ip','startTime','endTime' ,'range_time', 'dnsIp', 'requestId']

        alist = [{"startTime":{"$gt" : startTime, "$lt" : endTime }}]
        if requesturl: 
	    alist.append({'requestUrl':{'$regex' : requesturl}})
	if c_ip: 
	    alist.append({"client_ip": c_ip}) 

 
	if Num == 1000:
	    alist.append({"range_time":{"$lt":1000}})
	if Num == 2000:
	    alist.append({"range_time":{"$gt":1000,"$lt":2000}})
	if Num == 3000:
	    alist.append({"range_time":{"$gt":2000,"$lt":3000}})
	if Num == 3001:
	    alist.append({"range_time":{"$gt":3000}})


	mgo_ret = self.db[serapp_name].find({"$and":alist })

	full_url = (((self.request.full_url()).split("?"))[1]).lstrip("/")
	full_url = re.sub("page=(.*)", "page=" , full_url) 

	fen_ye = fenye.fen_ye_lei(page,[i for i in mgo_ret],10,11,5,'/chartsdetail/' +'?' + full_url ) 
	
        _dict = {"ret" : mgo_ret ,'tab_th_list':tab_th_list ,'timestamp_datetime':self.timestamp_datetime , 
	      'dqy':fen_ye.dang_qian_ye,'shuju':fen_ye.shu_ju_fan_wei(),'yem':fen_ye.xian_shi_ye_ma()
	    }


        if fen_ye.dang_qian_ye > fen_ye.zong_ye_ma:             
            zfchdqy = str(fen_ye.zong_ye_ma)                    
            self.redirect("/chartsdetail/" + zfchdqy +'?' + full_url)                  
        else:
            self.render('chartsdetail.html', **_dict)


    def post(self, *args,**kwargs):

	request_dict = self.request.arguments
	requestid = (request_dict['requestid'][0]).replace("\n","")
	allow_app = request_dict['allow_app'][0]
	api_type  = request_dict['api_type'][0]
	table_name = allow_app + '_' + api_type

	text = self.db[table_name].find({'requestId': requestid},{"_id":0})
	url_msg = [i for i in text][0]['requestUrl']

	self.write({'status':'ok','msg':url_msg})
       
