# -*- coding: utf-8 -*- 
import tornado.web
import MySQLdb ,json
import tornado.gen
from base import *





class AppOverview_Handler(BaseHandler):

    def get(self,*args, **kwargs):
	s = self.db.appnames.find({}).sort([('app_name',1)])

        current_user=self.get_current_user()
        f = self.db.project_privileges.find_one({"p1_list":{"$regex": current_user }},{"p2_list":1,"_id":0})
        ids = f['p2_list']

	__dict = {'applist': s ,'ids':ids}
        self.render('ovewview.html', **__dict)

class AppAdd_Handler(BaseHandler):

    def post(self,*args, **kwargs):
        request_dict = self.request.body
        names = json.loads(request_dict)

	#判断是否已经存在该app名称
        has_app = self.db.appnames.find_one({"app_name":  names['app_name']})
	if has_app:
	    self.db.appnames.find_one_and_delete({'_id': names['_id'] })


        collection = self.db.appnames
        result = collection.insert_one(names)
	self.write({'status':'ok', 'msg':'APP项目数据添加成功!!'})



class Appdelete_Handler(BaseHandler):
    def post(self):
        request_dict = self.request.arguments
        app_id = (request_dict['app_id'])[0]

	#删除已经存在该app名称
	self.db.appnames.delete_one({'_id': app_id})
	self.write('删除完成!!')	




class Appmod_Handler(BaseHandler):
    def post(self):
        request_dict = self.request.arguments
        app_id = (request_dict['app_id'])[0]
	data = self.db['appnames'].find_one({'_id':app_id})
	self.write(data)





