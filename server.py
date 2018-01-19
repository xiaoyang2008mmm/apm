# -*- coding: utf-8 -*- 
from   views import session
import tornado.httpserver, os
import tornado.ioloop
import tornado.web
from pymongo import MongoClient
from handlers.handlers import HANDLERS , STATIC_PATH , TEMPLATE_PATH

from tornado.options import define, options, parse_command_line
import ConfigParser,string,os,sys    
#报警子进程启动，定时执行
from  views.alarm import run

define("port", default=800, help="run on the given port", type=int)
define("dbfile", default="./conf/db.conf")

class Application(tornado.web.Application):
    def __init__(self):
	handlers=HANDLERS
	#初始化数据库连接
	cf = ConfigParser.ConfigParser()
	cf.read(options.dbfile)
	
	self.dbfile = options.dbfile
	db_host = cf.get("mongdb_db", "db_host")    
	db_port = cf.getint("mongdb_db", "db_port")    
	db_user = cf.get("mongdb_db", "db_user")    
	db_pass = cf.get("mongdb_db", "db_pass")

	redis_host = cf.get("redis", "redis_host")    
	redis_port = cf.getint("redis", "redis_port")    
	redis_pass = cf.get("redis", "redis_pass")

	settings = {                                                        
       	    "static_path": STATIC_PATH ,
     	    "template_path": TEMPLATE_PATH,
     	    "login_url": "/login/",                                                 
            "debug": True,                                                      
     	    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",                          
	    #"xsrf_cookies":True,                                                  
            'session_secret' :"3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
            'session_timeout': 6000,      #单位 秒
            'store_options' : {
                'redis_host': redis_host ,
                'redis_port': redis_port,
                'redis_pass': redis_pass
            },
	}                                                                   
                                                                    

     	tornado.web.Application.__init__(self, handlers, **settings)


        client = MongoClient(db_host , db_port)
        self.db = client.pinpoint

	self.session_manager = session.SessionManager(settings["session_secret"], settings["store_options"], settings["session_timeout"])

def main():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True,  ssl_options={
           "certfile": os.path.join(os.path.abspath("./cert/"), "214314540340956.pem"),
           "keyfile": os.path.join(os.path.abspath("./cert/"), "214314540340956.key"),
    })

    http_server.listen(options.port)
    tornado.ioloop.PeriodicCallback(run, 60000).start()  
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
