"""
	AdminHandler.py -- Admin portal
	
	by elchupathingy
"""

import tornado.web

class AdminHandler( tornado.web.RequestHandler ):
	def initialize( self, admins, pools, users ):
		self.pools = pools
		self.users = users
		self.admins = admins
		
	def get_login_url( self ):
		return "/login"
		
	def get_current_user(self):
		user = self.get_secure_cookie("user")
		
		if user:
			return user
		else:
			return None
		
	@tornado.web.authenticated
	def get( self, action ):
		if self.request.uri == "/admin":
			self.render( "./templates/admin.html", total_users=self.admins.totalAdmins(), total_miners=self.users.totalUsers(), total_pools=self.pools.totalPools(), total_shares=self.pools.totalShares() )
		elif self.request.uri == "/admin/manusers":
			self.render( "./templates/adminusers.html", users=self.admins )
		elif self.request.uri == "/admin/manminers":
			self.render( "./templates/adminminers.html", users=self.users )
		elif self.request.uri == "/admin/manpools":
			self.render( "./templates/adminpools.html", pools=self.pools )

	@tornado.web.authenticated
	def post( self ):
		pass