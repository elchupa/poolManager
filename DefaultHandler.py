"""
	DefaultHandler -- The Home page for the frontend.
	
	by elchupathingy
"""

import tornado.web

class DefaultHandler( tornado.web.RequestHandler ):
	def initialize( self, sharedb, userdb, poolname ):
		self.pooldb = sharedb
		self.userdb = userdb
		self.poolname = poolname
	
	def get( self ):
		
		if self.request.uri == "/":
			self.render( "./templates/index.html" )
		elif self.request.uri == "/getusers":
			users = self.userdb.getAll()
			self.render( "./templates/users.html", users=users )
		elif self.request.uri == "/getpools":
			pools = self.pooldb.getAll()
			self.render( "./templates/pools.html", pools=pools )