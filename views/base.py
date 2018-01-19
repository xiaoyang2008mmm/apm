# -*- coding: utf-8 -*- 

import tornado.web
import  time
from pymongo import MongoClient
import session

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.session = session.Session(self.application.session_manager, self)

    def prepare(self):

	#针对api接口 做特殊处理，不走验证
	if "/api/interface/"  in  self.request.uri: 
	    return

	#其余走http验证
	if not self.request.uri.startswith(self.get_login_url()) and not self.session.get("username")  and self.get_current_user() is  None:
            self.redirect(self.get_login_url())

	#没有权限返回403

	get_allow_url = self.get_allow_url()
	alist = self.getallpage_urls()
	
	if self.request.uri in alist  and  self.request.uri not in get_allow_url:
	    raise tornado.web.HTTPError(403)

    def get_current_user(self):
        if self.session.get("username"):
            return  self.session.get("username")
	return None
	
    def tab_fix(self):
	return self.session.get("table_prefix")

    @property
    def db(self):
        return self.application.db

    @property
    def dbfile(self):
        return self.application.dbfile

    def get(self):
        self.write_error(404)



    def write_error(self, status_code, **kwargs):
        self.render('exception.html', status_code = status_code )


    def datetime_timestamp(self,dt):
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s * 1000)

    def timestamp_datetime(self,value):
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(value / 1000)
        dt = time.strftime(format, value)
        return dt

    def get_allow_url(self):
	login_user = self.get_current_user()
	if login_user is None:
	    login_user = "*"
	
	s = self.db.sys_privileges.find({"userlist":{"$regex": login_user }},{"urllist":1,"_id":0})
	pvlist = []
	for pv in s:
	    pvlist += pv['urllist']

	pvlist = [ i.encode("utf8")  for i in (list(set(pvlist)))]

	return  pvlist

    def allmenus(self): 
	sys_menuall = self.db.sys_menu.find({},{"_id":0})
	return sys_menuall	

    def getallpage_urls(self):
	sys_menuall = self.db.sys_menu.find({},{"_id":0})
	indexlist = []
	for a in sys_menuall:
	    for b in a:
		for c in a[b]:
		    indexlist.append(c[1])
	return  list(set(indexlist))
    
    def get_appallserverip(self):
	try:
            ips = self.db['appnames'].find({'app_table_name': self.tab_fix()},{"_id":0})
            ret_ip = [ip for ip in ips][0]
	    return ret_ip
	except:
	    return None


    def get_allowapps(self):

        current_user=self.get_current_user()
     	if current_user :
            s = self.db['project_privileges'].find_one({"p1_list":{"$regex": current_user }},{"p2_list":1,"_id":0})
	    if s is None:
	        return [] 
            return  s['p2_list']

	else:
	    return []

    #模板全局变量
    def get_template_namespace(self):
        namespace = {}
        namespace = super(BaseHandler,self).get_template_namespace()
        uimethods={
            "allow_urls": self.get_allow_url(),
	    "all_ips": self.get_appallserverip(),
	    "tab_fix": self.tab_fix() ,
	    "allmenus": self.allmenus(),
	    'allowapps': self.get_allowapps()
        }
        namespace.update(uimethods)
        return namespace
