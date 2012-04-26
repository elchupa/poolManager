"""
	LoginHandler.py -- Handlers admin authentication.
	
	by elchupathingy
"""

import tornado.web
import logging
from datetime import datetime

class LoginHandler(tornado.web.RequestHandler):
	
	def initialize( self ):
		self.admins = self.application.admins
		self.logger = logging.getLogger( "PoolManager.Http.LoginHandler" )
		
	def get( self ):
			self.render( "./templates/login.html", next=self.get_argument("next", u"/") )

	def post( self ):
		username = self.get_argument("username", "")
		password = self.get_argument("password", "")
		auth = self.admins.getUser(username, password)
		if auth != None:
			self.set_current_user( username )
			print self.get_argument("next", u"/")
			self.redirect( self.get_argument("next", u"/") )
		else:
			error_msg = "?next=" + self.get_argument("next", u"/") + "&error=" + tornado.escape.url_escape("Login incorrect.")
			self.redirect(u"/login" + error_msg )

	def set_current_user(self, user):
		if user:
			self.set_secure_cookie( "lasttime", str( datetime.now() ) )
			self.set_secure_cookie("user", tornado.escape.json_encode(user))
		else:
			self.clear_cookie("user")
