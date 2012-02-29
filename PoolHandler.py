"""
	PoolHandler.py -- Individual Pool Stats
	
	by elchupathingy
"""

import tornado.web

import logging

class PoolHandler( tornado.web.RequestHandler ):
	def initialize( self, pools, users ):
		self.pools = pools
		self.users = users
		
		self.logging = logging.getLogger( "PoolManager.Http.PoolHandler" )
	
	def get( self, poolname ):
		poolname = poolname.replace( "+", " " )
		pool = self.pools.getPool( poolname )
		users = self.users.getUsers( pool['users'] )
		
		self.render( "./templates/pool.html", pool=pool, users=users )