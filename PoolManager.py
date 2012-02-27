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
from PoolHandler import PoolHandler

class PoolManager:
	def __init__( self, config ):
		self.config = Config( config )
		self.users = UserStore( config )
		self.pools = PoolStore( config, self.users )
		self.admins = AdminStore( config )
		
		self.getworkApp = tornado.web.Application( [ (r"/", GetWorkHandler, dict(sharedb=self.pools, usersdb=self.users, poolname="mine") ) ], debug=True )
		
		self.getworkServer = tornado.httpserver.HTTPServer(self.getworkApp)
		
		self.frontendApp = tornado.web.Application( 
		[ 
			( r"/", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="mine" ) ),
			( r"/getusers", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="mine" ) ),
			( r"/getpools", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="mine" ) ),
			( r"/admin", AdminHandler, dict( pools=self.pools, users=self.users ) ),
			( r"/login/?(\w\d)", LoginHandler, dict( admins=self.admins ) ),
			( r"/pool/([\w\d]+)", PoolHandler, dict( pools=self.pools, users=self.users ) )
		], debug=True )
		
		self.frontendServer = tornado.httpserver.HTTPServer( self.frontendApp )
		
		self.getworkServer.listen( self.config['pool']['port'] )
		self.frontendServer.listen( self.config['http']['port'] )
		
		tornado.ioloop.IOLoop.instance().start()
		
if __name__ == "__main__":
	p = PoolManager( "config.json" )