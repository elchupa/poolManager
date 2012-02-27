"""
	LoginHandler.py -- Handlers admin authentication.
	
	by elchupathingy
"""

import tornado.web

class LoginHandler(tornado.web.RequestHandler):
	
	def initialize( self, admins ):
		self.admins = admins

    def get(self, error ):
        self.render( "login.html", error=error )

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.admins.getUser(username, password)
        if auth != None:
            self.set_current_user(username)
            self.redirect( "/userpanel" )
        else:
            error_msg = tornado.escape.url_escape("incorrect")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")