# -*- coding: utf-8 -*- 
import tornado.web
import MySQLdb ,json
import tornado.gen
from  ldap3 import *
from base import *
import base64
import ConfigParser





class Login_Handler(BaseHandler):
    """登录验证"""
    def get(self):
        self.render('userlogin.html')
    def post(self):

        cf = ConfigParser.ConfigParser()
        cf.read(self.dbfile)
        ldap_host = cf.get("ldap", "ldap_host")    
        ldap_port = cf.getint("ldap", "ldap_port")    
        ldap_user = cf.get("ldap", "ldap_user")    
        ldap_pass = cf.get("ldap", "ldap_pass")
	ret = json.loads(self.request.body)
	LDAP_SERVER = ldap_host
	server = Server(LDAP_SERVER, use_ssl=False)
	cninfo = 'cn=%s,dc=9icaishi,dc=net'%(ldap_user)
	conn = Connection(server, cninfo, ldap_pass, auto_bind=True)
	
	
	#验证用户
	username = ret['login_username']
	password = ret['login_password'].encode("utf8")
	base = "uid={},ou=People,dc=9icaishi,dc=net".format(username)
	conn.search(base, search_filter="(uid={})".format(username))
	conn.entries
	
	ldap_ret  =  conn.rebind(base, password)
	if ldap_ret:
            self.session["username"] = username
            self.session.save()
            self.write({'status':'ok'})
            self.finish()
        else:
	    #起用本地系统认证
	    get_pwd = self.db['sysuser'].find_one({"sysuser_name": username}, {"sysuser_pwd":1,"_id":0})
            passwd = get_pwd['sysuser_pwd']
            result = base64.decodestring(passwd)
	    if password == result:
	    	self.session["username"] = username
            	self.session.save()
            	self.write({'status':'ok'})
		return 

            self.write({'status':'error', 'msg':'用户名或者密码错误,请联系管理员进行处理!'})


class Logout_Handler(BaseHandler):

    """退出"""

    def post(self):
	self.session["username"] = None
	self.session.save()
	ret = json.loads(self.request.body)
	self.write({'status':'ok'})




class projectCheckout_Handler(BaseHandler):

    def post(self,*args, **kwargs):
        request_dict = self.request.arguments
	app = request_dict['app'][0]
	s = self.db.appnames.find({"app_name": app },{"app_table_name":1,"_id":0})
	table_prefix = ([i for i in s][0])['app_table_name'] 
	
	table_set = self.db.collection_names()
	list0 = [i for i in table_set  if table_prefix in i ]
	if list0:
            self.session["table_prefix"] = table_prefix  
            self.session.save()
	    self.write({'status':'ok','msg':table_prefix})
	else:
	    self.write({'status':'error'})







class fileauthURL_Handler(BaseHandler):
    """证书验证"""
    def get(self):
        self.render('fileauth.txt')










class ChPasswd_Handler(BaseHandler):

    def get(self,*args, **kwargs):
        self.render('changepwd.html')

    def post(self,*args, **kwargs):
	ret = json.loads(self.request.body)
	account_source = ret['account_from']
	get_loginuser = ret['get_loginuser']
	passwd = base64.encodestring(ret['passwd_1'])

	if 'apm' in account_source:
	    self.db.sysuser.find_one_and_update({'sysuser_name':get_loginuser },{'$set': {'sysuser_pwd': passwd}})
	    self.write({'status':'ok','msg':'处理中'})
	if 'ldap' in account_source:
	    self.write({'status':'ok','msg':'ldap账号密码暂不支持修改!!'})
