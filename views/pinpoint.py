# -*- coding: utf-8 -*- 

import tornado.web
from get_data  import Pinpoint_data
import  json,requests
import  time
from base import *





class PP_Handler(BaseHandler):

    def get_pinpoint_ip(self):
	return  '10.2.2.102:8080' 

    def get(self):
	pp= Pinpoint_data(self.get_pinpoint_ip())
	pp_name =  json.loads(pp.get_ppagent())
	_dict = {'pp_names': pp_name}
        self.render('pp.html', **_dict)

    def post(self):
        request_dict = self.request.arguments

	p_name = request_dict['p_name'][0]
	ppstarttime = request_dict['ppstarttime'][0]
	ppendtime = request_dict['ppendtime'][0]

	#增加时间检测
        etime   =  int(time.time() * 1000)
        stime =  etime - (5 * 60000) 
	if ppstarttime:
	     stime = self.datetime_timestamp(ppstarttime)
	if ppendtime:
	     etime = self.datetime_timestamp(ppendtime)

	pp = Pinpoint_data(self.get_pinpoint_ip(), application=p_name ,starttime=stime , endtime=etime)
	data = pp.main()
	if data:
	     self.write({'status':'OK','msg': data})
	else:
	     self.write({'status':'ERROR'})



class TransactionId_Handler(BaseHandler):

    def get_ppip(self):
	return '10.2.2.102:8080' 
	   
	
    def get(self,*args, **kwargs):
        request_dict = self.request.arguments
	self.get_ppip()
	try:
	    trac_id = request_dict['id'][0]
	except:
	    _dict = {'tids': None ,'trac_id': None}
            self.render('transactionId.html', **_dict)
	    return 
	
	url = 'http://{0}/transactionInfo.pinpoint?traceId={1}'.format(self.get_ppip(), trac_id)
	rr = requests.get(url)
	data = (json.loads(rr.text))['callStack']

	_dict = {'tids': data ,'trac_id':trac_id}
        self.render('transactionId.html', **_dict)

    def post(self,*args, **kwargs):
        request_dict = self.request.arguments
	trac_id = request_dict['traceid'][0]
	url = 'http://{0}/transactionInfo.pinpoint?traceId={1}'.format(self.get_ppip(), trac_id)
	rr = requests.get(url)
	data = json.loads(rr.text)
	self.write(data)
