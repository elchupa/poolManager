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
		users = self.userdb.getAll()
		self.write( "<table>" )
		for user in users:
			self.write( "<tr><td>Username: " + user['username'] + "</td><td>Shares: " + str( user['shares'] ) + "</td><td>Last Share Time: " + str( user['lastShare'] ) + "</td></tr>" )
		self.write( "</table>" )