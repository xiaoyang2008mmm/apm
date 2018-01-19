# -*- coding: utf-8 -*- 
import tornado.web
import MySQLdb ,json
import tornado.gen
import base64, os
from base import *
from  ldap3 import *
import ConfigParser


class SystemUser_Handler(BaseHandler):

    def get(self,*args, **kwargs):
	plist_table = self.db['project_privileges'].find({})
	syslist_table = self.db['sys_privileges'].find({})
	sys_menuall = self.db.sys_menu.find({},{"_id":0})

	maplist = [ l.values()[0] for l in sys_menuall]
        __dict = {'applist': self.get_applist , 'plist_table':plist_table ,'syslist_table':syslist_table, 'maplist':maplist }

        self.render('sys_user.html', **__dict)

    def get_applist(self):
	s1 = self.db.appnames.find({}).sort([('app_name',1)])
	return s1

    def post(self,*args, **kwargs):
        ret = json.loads(self.request.body)

        collection = self.db['project_privileges']
        result = collection.insert_one(ret)
	self.write("ok")
	

class AddSysuser_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	ret = json.loads(self.request.body)
        collection = self.db['sysuser']

	#做密码加密处理
	base_passwd = base64.encodestring(ret['sysuser_pwd'])
	ret['sysuser_pwd'] = base_passwd 
        result = collection.insert_one(ret)

        self.write({'status':'ok','msg': '系统用户添加完成!'})

class AjaxUserList_Handler(BaseHandler):

    def get(self,*args, **kwargs):	
	request_dict = self.request.arguments
	t = request_dict['type'][0]
	if t == 'ldap':
            cf = ConfigParser.ConfigParser()
            cf.read(self.dbfile)
            ldap_host = cf.get("ldap", "ldap_host")
            ldap_port = cf.getint("ldap", "ldap_port")
            ldap_user = cf.get("ldap", "ldap_user")
            ldap_pass = cf.get("ldap", "ldap_pass")
            LDAP_SERVER = ldap_host
            server = Server(LDAP_SERVER, use_ssl=False)
            cninfo = 'cn=%s,dc=9icaishi,dc=net'%(ldap_user)
            conn = Connection(server, cninfo, ldap_pass, auto_bind=True)

	    base = "ou=People,dc=9icaishi,dc=net"
	    get_all_user = conn.search(search_base=base,
                         search_filter="(uid=*)",
                         attributes=['mail', 'uid', 'ou']
                         )

	    ret = get_all_user
	    user_info = [[entry.uid.values[0],  entry.mail.values[0] ]
                    for entry in conn.entries]
	if t == 'apm':	
	    uret = self.db['sysuser'].find({})
	    user_info = [[entry['sysuser_name'],  entry['sysuser_email'] ]
                    for entry in uret]

	s = { "data": user_info }
	
	self.write(json.dumps(s))



class Pnamedelete_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	request_dict = self.request.arguments
        pgroup_name = (request_dict['pgroup_name'])[0]

        self.db.project_privileges.delete_one({'p0': pgroup_name})
        self.write('删除完成!!')



class Pnamealter_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	request_dict = self.request.arguments
        pgroup_name = (request_dict['pgroup_name'])[0]

	app = self.db.project_privileges.find_one({'p0': pgroup_name},{"_id":0})
	self.write(app)




class Create_roles_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	ret = json.loads(self.request.body)
        collection = self.db['sys_privileges']
	collection.find_one_and_delete({'name':ret['name']})
        result = collection.insert_one(ret)
	self.write({'status':'ok'})	




class Delete_Roles_group_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	request_dict = self.request.arguments
        sname = (request_dict['sname'])[0]

        self.db.sys_privileges.delete_one({'name': sname})
        self.write('删除完成!!')




class SystemMail_Handler(BaseHandler):

    def get(self,*args, **kwargs):
        cf = ConfigParser.ConfigParser()
	filename = os.getcwd() + '/conf/mail.conf'
        cf.read(filename)

        smtpserver = cf.get("smtp", "smtpserver")
        smtpaccount = cf.get("smtp", "smtpaccount")
        smtppwd = cf.get("smtp", "smtppwd")

	_dict = {"smtpserver":smtpserver, "smtpaccount":smtpaccount, "smtppwd":smtppwd }

	self.render('sys_mail.html', **_dict)

    def post(self,*args, **kwargs):
	ret = json.loads(self.request.body)
	cf = ConfigParser.ConfigParser()
	
	filename = os.getcwd() + '/conf/mail.conf'
	cf.read(filename)
	cf.set("smtp", "smtpserver", ret['smtpserver'])           
	cf.set("smtp", "smtpaccount", ret['smtpaccount'])           
	cf.set("smtp", "smtppwd", ret['smtppwd'])           
	
	with open(filename,"w+") as f:
	    cf.write(f)

	self.write("保存成功!!!")




class SystemMenu_Handler(BaseHandler):

    def get(self,*args, **kwargs):
	menus = self.db.sys_menu.find({},{"_id":0})
	self.render('sys_menu.html',menus = menus)

    def post(self,*args, **kwargs):
	ret = json.loads(self.request.body)
	menu_title = ret['menu_one']	
	s = self.db.sys_menu.find({},{menu_title :1,"_id":0})
	ret = [i  for i in s if i][0]

	self.write(ret)



class AddoneMenu_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	request_dict = self.request.arguments
	if request_dict.has_key('newonemenu'):
            newonemenu = (request_dict['newonemenu'])[0]
	    aname = {newonemenu:[]}
	    self.db.sys_menu.insert_one(aname)
	    self.write({'status':'ok','msg':'保存成功!!!'})
	if request_dict.has_key('newtwoname'):

            newtwoname = (request_dict['newtwoname'][0]).decode("utf8")
            newtwourl = (request_dict['newtwourl'][0]).decode("utf8")
            menu_title = (request_dict['menu_one'][0]).decode("utf8")
            s1 = self.db.sys_menu.find({},{menu_title :1,"_id":0})
            s2 = self.db.sys_menu.find({},{menu_title :1,"_id":0})
            ret = [i  for i in s1 if i][0]
            beset = [i  for i in s2 if i][0]

	    urls_list = ret[menu_title]
	    if urls_list:
		urls_list.append([newtwoname, newtwourl])
	    else:
		urls_list=[[newtwoname, newtwourl]]

	    self.db.sys_menu.replace_one(beset , {menu_title: urls_list})
	    self.write({'status':'ok','msg':'二级菜单添加成功!!!'})




class DeleteMenu_Handler(BaseHandler):

    def post(self,*args, **kwargs):	
	request_dict = self.request.arguments
	if request_dict.has_key('two_name'):

            two_name = (request_dict['two_name'][0]).decode("utf8")
            two_url = (request_dict['two_url'][0]).decode("utf8")
            menu_title = (request_dict['menu_one'][0]).decode("utf8")

            s1 = self.db['sys_menu'].find({},{menu_title :1,"_id":0})
            ret = [i  for i in s1 if i][0]
            s2 = self.db.sys_menu.find({},{menu_title :1,"_id":0})
            beset = [i  for i in s2 if i][0]

	    clear_list = [two_name,two_url]
            urls_list = ret[menu_title]

	    for i in urls_list:
		if i == clear_list:
		    urls_list.remove(i)

	    self.db.sys_menu.replace_one(beset , {menu_title: urls_list})
            self.write({'status':'ok','msg':'二级菜单删除成功!!!'})
