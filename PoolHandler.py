"""
	PoolHandler.py -- Individual Pool Stats
	
	by elchupathingy
"""

import tornado.web

class PoolHandler( tornado.web.RequestHandler ):
	def initialize( self, pools, users ):
		self.pools = pools
		self.users = users
	
	def get( self, poolname ):
		poolname = poolname.replace( "+", " " )
		pool = self.pools.getPool( poolname )
		users = self.users.getUsers( pool['users'] )
		
		self.render( "./templates/pool.html", pool=pool, users=users )