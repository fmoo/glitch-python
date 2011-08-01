from google.appengine.ext import webapp
from urllib import urlencode

class BaseHandler(webapp.RequestHandler):
    def go_home(self, msg=None):
        if msg:
            encoded = urlencode({'error_msg': msg})
            self.redirect('/?' + encoded)
        else:
            self.redirect('/')
