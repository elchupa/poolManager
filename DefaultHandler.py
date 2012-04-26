"""
	DefaultHandler -- The Home page for the frontend.
	
	by elchupathingy
"""

import tornado.web

import logging

class DefaultHandler( tornado.web.RequestHandler ):
	def initialize( self ):
		self.pooldb = self.application.pools
		self.userdb = self.application.users
		self.poolname = self.application.poolname
		
		self.logger = logging.getLogger( "PoolManager.Http.DefaultHandler" )
		
	def get( self ):
		self.logger.debug( "Got A Request to the home page" )
		if self.request.uri == "/":
			self.render( "./templates/index.html" )
		elif self.request.uri == "/getusers":
			users = self.userdb.getAll()
			self.render( "./templates/users.html", users=users, totalShares=self.userdb.totalShares() )
		elif self.request.uri == "/getpools":
			pools = self.pooldb.getAll()
			self.render( "./templates/pools.html", pools=pools, totalShares=self.pooldb.totalShares() )
