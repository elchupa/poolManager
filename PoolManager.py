"""
	PoolManager.py -- Loads the database adn config settings and starts
	the services.
	
	by elchupathingy
"""
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from PoolStore import PoolStore
from UserStore import UserStore
from AdminStore import AdminStore
from Config import Config

from GetWorkProxy import GetWorkHandler
from DefaultHandler import DefaultHandler
from AdminHandler import AdminHandler
from LoginHandler import LoginHandler
from PoolHandler import PoolHandler
import base64
import uuid

class PoolManager:
	def __init__( self, config ):
		self.config = Config( config )
		self.users = UserStore( config )
		self.pools = PoolStore( config, self.users )
		self.admins = AdminStore( config )
		
		self.getworkApp = tornado.web.Application( [ (r"/", GetWorkHandler, dict(sharedb=self.pools, usersdb=self.users, poolname="triplemining.com" ) ) ], debug=True )
		
		self.getworkServer = tornado.httpserver.HTTPServer(self.getworkApp)
		
		settings = {
			"cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
			"login_url": "/login"
		}
		
		self.frontendApp = tornado.web.Application( 
		[ 
			( r"/", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="triplemining.com" ) ),
			( r"/getusers", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="triplemining.com" ) ),
			( r"/getpools", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="triplemining.com" ) ),
			( r"/admin(/[\w\d]+)?", AdminHandler, dict( admins=self.admins,pools=self.pools, users=self.users ) ),
			( r"/login", LoginHandler, dict( admins=self.admins ) ),
			( r"/pool/([\w\d\.]+)", PoolHandler, dict( pools=self.pools, users=self.users ) )
		], **settings )
		
		self.frontendServer = tornado.httpserver.HTTPServer( self.frontendApp )
		
		self.getworkServer.listen( self.config['pool']['port'] )
		self.frontendServer.listen( self.config['http']['port'] )
		
		tornado.ioloop.IOLoop.instance().start()
		
if __name__ == "__main__":
	p = PoolManager( "config.json" )