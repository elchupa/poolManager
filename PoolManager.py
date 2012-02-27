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
from Config import Config

from GetWorkProxy import GetWorkHandler
from DefaultHandler import DefaultHandler

class PoolManager:
	def __init__( self, config ):
		self.config = Config( config )
		self.users = UserStore( config )
		self.pools = PoolStore( config )
		
		self.getworkApp = tornado.web.Application( [ (r"/", GetWorkHandler, dict(sharedb=self.pools, usersdb=self.users, poolname="mine") ) ], debug=True )
		
		self.getworkServer = tornado.httpserver.HTTPServer(self.getworkApp)
		
		self.frontendApp = tornado.web.Application( [ ( r"/", DefaultHandler, dict( sharedb=self.pools, userdb=self.users, poolname="mine" ) ) ], debug=True )
		
		self.frontendServer = tornado.httpserver.HTTPServer( self.frontendApp )
		
		self.getworkServer.listen( self.config['pool']['port'] )
		self.frontendServer.listen( self.config['http']['port'] )
		
		tornado.ioloop.IOLoop.instance().start()
		
if __name__ == "__main__":
	p = PoolManager( "config.json" )