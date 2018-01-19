#coding=utf-8 
import requests
import  json ,time
from operator import itemgetter
    
    

class Pinpoint_data(object):

    def __init__(self, ppip,application=None ,starttime=None, endtime=None):
        self.pinpoint_url = 'http://' + ppip               #pinponit服务地址
        self.application = application    	#到页面f12获取查看
        self.xGroupUnit = 987                   #到页面f12获取查看
        self.yGroupUnit = 57                    #到页面f12获取查看
        self.limit = 50000                        #请求数据条数控制
  
	self.from_time = starttime 
	self.to_time = endtime
	

    def get_getScatterData(self):

        url = self.pinpoint_url + '/getScatterData.pinpoint'
        
        data =  {
            'to':               self.to_time,
            'from':             self.from_time,
            'limit':            self.limit,
            'application':      self.application,
            'xGroupUnit':       self.xGroupUnit,
            'yGroupUnit':       self.yGroupUnit
        }
        
        headers = {  
                'Content-Type': 'application/json',
            }  
        
        r = requests.get(url, params=data)
	data = json.loads(r.text)
	ret = data['scatter']
	dotList =  ret['dotList']
	metadata = ret['metadata']

	#获取请求时间, 获取agent采集时间, 获取tractionid 拼成元祖列表
	getapi_list=[(i[0],i[1],i[2],i[3]) for i in dotList]
	#获取访问耗时 Top20
	getapi_list.sort(key = lambda x: x[1], reverse = True)
        s =[]
	for l in getapi_list[:20]:
      	    g = metadata[str(l[2])]
    	    TransactionId = str(g[1]) + '^' + str(g[2]) + '^' + str(l[3])
	    ret = {'elapsed':l[1], 'traceId':TransactionId ,'span':'<span class="glyphicon glyphicon-arrow-right"></span>'}
    	    s.append(ret) 
	return s
        
        
    
    
    
    def main(self):

        data = self.get_getScatterData()
        return data 
    

    def get_ppagent(self):

	url = self.pinpoint_url + '/applications.pinpoint'
	data = requests.get(url)
	return (data.text)
    
