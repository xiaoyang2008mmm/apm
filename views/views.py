# -*- coding: utf-8 -*- 

import tornado.web
import MySQLdb ,json
import requests
from base import *

class Index_Handler(BaseHandler):
    def get(self):
        self.render('index.html') 
       
class Base_Handler(BaseHandler):

    def get(self):
        current_user = self.get_current_user()
	
	_dict = { 'current_user' : current_user}
        self.render("base.html", **_dict)


class getIpInfo_Handler(BaseHandler):

    def post(self):
        request_dict = self.request.arguments
        ip = ((request_dict['ip'])[0]).replace(" ","")

	url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ip
        r = requests.get(url)
	data = (json.loads(r.text))['data']
        country = data['country']  	#国家 
        area = data['area']    		#区域
        region = data['region']    	#地区
        city = data['city']    		#城市
        isp = data['isp']      		#运营商
        msg = u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (country, area, region, city, isp)
	self.write(msg)


class Pvdetail_Handler(BaseHandler):

    def get(self):
        self.render('apmpv.html') 
