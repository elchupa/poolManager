"""
	AdminHandler.py -- Admin portal
	
	by elchupathingy
"""

import tornado.web

class AdminHandler( tornado.web.RequestHandler ):
	def initialize( self, pools, users ):
		self.pools = pools
		self.users = users
		
	def get_login_url( self ):
		return "/login"
		
	def get( self ):
		self.write( "Adming panel" )