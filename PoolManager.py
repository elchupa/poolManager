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

from GetWorkHandler import GetWorkHandler
from LongPollHandler import LongPollHandler
from DefaultHandler import DefaultHandler
from AdminHandler import AdminHandler
from LoginHandler import LoginHandler
from PoolHandler import PoolHandler

from LongPoll import LongPoll

import logging

import base64
import uuid

import logging

class PoolManager:
	def __init__( self, config ):
		self.config = Config( config )
		self.users = UserStore( config )
		self.pools = PoolStore( config, self.users )
		self.admins = AdminStore( config )
		
		console = logging.StreamHandler()
		formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')
		console.setFormatter( formatter )
		logging.getLogger('').addHandler( console )
		
		LEVELS = {
					'debug': logging.DEBUG,
					'info': logging.INFO,
					'warning': logging.WARNING,
					'error': logging.ERROR,
					'critical': logging.CRITICAL
				}
		#if "logFile" in self.config:
		#	fileHandler = logging.FileHandle( str( self.config['logFile'] ) )
		#	fileHandler.setFormatter( formatter )
		#	logging.getLogger('').addHandler( fileHandler )
		
		self.logger = logging.getLogger( "PoolManager" )
		
		try:
			self.logger.setLevel( LEVELS[self.config['logLevel']] )
		except:
			self.logger.setLevel( logging.ERROR )
		
		
		self.logger.info( "PoolManager Started" )
		self.logger.info( "Creating Tornado Applications" )
		self.longpoll = LongPoll( self.pools, "triplemining.com" )
		
		self.getworkApp = tornado.web.Application( [ 
		(r"/", GetWorkHandler, dict(sharedb=self.pools, usersdb=self.users, poolname="triplemining.com", longpoll = self.longpoll ) ),
		( r"/LP", LongPollHandler, dict( pools=self.pools, users=self.users, poolname="triplemining.com", longpoll = self.longpoll ) )
		] )
		
		self.logger.info( "Creating HTTPServers for the Web interfave and the pool backend." )
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
			( r"/admin(/[\w\d\+%]+)?", AdminHandler, dict( admins=self.admins,pools=self.pools, users=self.users ) ),
			( r"/login", LoginHandler, dict( admins=self.admins ) ),
			( r"/pool/([\w\d\.\+ %]+)", PoolHandler, dict( pools=self.pools, users=self.users ) ),
		], **settings )
		
		self.frontendServer = tornado.httpserver.HTTPServer( self.frontendApp )
		
		self.logger.info( "Pool Running On Port ( %d )", self.config['pool']['port'] )
		self.getworkServer.listen( self.config['pool']['port'] )
		self.logger.info( "Web Interface Running On Port ( %d )", self.config['http']['port'] )
		self.frontendServer.listen( self.config['http']['port'] )
		
		self.logger.info( "Starting IOLoop" )
		tornado.ioloop.IOLoop.instance().start()
		
if __name__ == "__main__":
	p = PoolManager( "config.json" )