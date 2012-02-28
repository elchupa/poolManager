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
			self.render( "./templates/adminusers.html", users=self.admins.getAll(), error="" )
		elif self.request.uri == "/admin/manminers":
			users = self.admins.getAll()
			self.render( "./templates/adminminers.html", users=self.users.getAll(), error="" )
		elif self.request.uri == "/admin/manpools":
			self.render( "./templates/adminpools.html", pools=self.pools.getAll(), error="" )

	@tornado.web.authenticated
	def post( self, page ):
		error = ""
		submit = self.get_argument( "submit" )
		if page == "/manusers":
			if submit == "Add User":
				user = self.get_argument( "user" )
				password = self.get_argument( "password1" )
				password2 = self.get_argument( "password2" )
			
				if password != password2:
					error = "<font color='red'>Passwords do not match</font><br />"
					self.render( "./templates/adminusers.html", users.self.admins.getAll(), error=error )
				else:
					self.admins.addUser( user, password )
					error = "<font color='green'>" + str( user ) + " successfully added.</font><br />"
					self.render( "./templates/adminusers.html", users=self.admins.getAll(), error=error )
			elif submit == "Delete":
				val = self.admins.collection.remove( { "username": self.get_argument( "user" ), "level": { "$gt": 0 } } )
				self.write( str( self.get_argument( "user" ) ) )
		elif page == "/manminers":
			if submit == "Add Miner":
				user = self.get_argument( "user" )
				password = self.get_argument( "password" )
				owner = self.get_argument( "owner" )
				
				user = self.users.getUser( user, password, owner )
				
				error = "<font color='green'>" + str( user ) + " successfully added.</font><br />"
				self.render( "./templates/adminminers.html", users=self.users.getAll(), error=error )
			elif submit == "Delete":
				user = self.get_argument( "miner" )
				val = self.users.collection.remove( { "username": user } )
				
				self.write( str( user ) )
		elif page == "/manpools":
			if submit == "Add Pool":
				name = self.get_argument( "name" )
				address = self.get_argument( "address" )
				port = int( self.get_argument( "port" ) )
				username = self.get_argument( "username" )
				password = self.get_argument( "password" )
				timeout = int( self.get_argument( "timeout" ) )
				
				self.pools.addPool( name, address, port, username, password, timeout )
				
				error = "<font color='green'>" + str( name ) + " successfully added.</font><br />"
				self.render( "./templates/adminpools.html", pools=self.pools.getAll(), error=error )
			elif submit == "Delete":
				pool = self.get_argument( "pool" )
				val = self.pools.collection.remove( { "name": pool } )
				
				self.write( str( pool ) )