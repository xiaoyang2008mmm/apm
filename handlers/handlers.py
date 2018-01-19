# -*- coding: utf-8 -*- 
from views.views   import *
from views.api     import *
from views.charts  import *
from views.pinpoint import *
from views.index   import *
from views.monitor import * 
from views.system  import * 
from views.auth    import * 
from views.rules   import *
import os.path

STATIC_PATH   = os.path.join(os.path.dirname(__file__), "../static")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
HANDLERS =[(  r"/", 				Index_Handler),
	   (  r"/base/",  			Base_Handler),
	   (  r"/api/interface/get_config/",	GetConfigHandler),
	   (  r"/api/interface/(.*)",  		InterfaceHandler),
	   (  r"/perf/interface/",  		getdata_Handler),
	   (  r"/chartsdetail/",  		Chartsdetail_Handler),
	   (  r"/getIpInfo/",  			getIpInfo_Handler),
	   (  r"/pinpoint/",  			PP_Handler),
	   (  r"/transactionId/(.*)",  		TransactionId_Handler),
	   (  r"/pv_count/",  			Pvdetail_Handler),
	   (  r"/app/overview/",  		AppOverview_Handler),
	   (  r"/app_add/",  			AppAdd_Handler),
	   (  r"/app_operation/delete/",  	Appdelete_Handler),
	   (  r"/app_operation/mod/",  		Appmod_Handler),
	   (  r"/app/monitor/",  		AppMonitor_Handler),
	   (  r"/apps/rules/add/",  		AppRulesAdd_Handler),
	   (  r"/apps/rules/apply/",  		AppRulesApply_Handler),
	   (  r"/system/user/(.*)",  		SystemUser_Handler),
	   (  r"/system/mail/",  		SystemMail_Handler),
	   (  r"/system/menu/",  		SystemMenu_Handler),
	   (  r"/system/menu/add/",  		AddoneMenu_Handler),
	   (  r"/system/menu/delete/",  	DeleteMenu_Handler),
           (  r"/login/",                 	Login_Handler),
           (  r"/logout/",                	Logout_Handler),
           (  r"/auth/changepasswd/",           ChPasswd_Handler),
           (  r"/ajax/user/list",               AjaxUserList_Handler),
           (  r"/add_sysuser/",                 AddSysuser_Handler),
           (  r"/pname/delete/",          	Pnamedelete_Handler),
           (  r"/pname/alter/",          	Pnamealter_Handler),
           (  r"/create_roles/",          	Create_roles_Handler),
           (  r"/delete_roles_group/",         	Delete_Roles_group_Handler),
           #项目权限检查
           (  r"/project/appprivileges_check/",                 projectCheckout_Handler),
	   #证书校验
           (  r"/.well-known/pki-validation/fileauth.txt",    	fileauthURL_Handler),
	   #404处理,一定放在末尾
	   (r".*", 				BaseHandler),
	   
	
	]
