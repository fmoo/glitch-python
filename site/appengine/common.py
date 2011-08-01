from google.appengine.ext import webapp
from urllib import urlencode

from glitch.datetime import GlitchDateTime

from google.appengine.ext.webapp.template \
       import register_template_library
register_template_library('django.contrib.humanize.templatetags.humanize')


class BaseHandler(webapp.RequestHandler):
    def default_data(self):
        d = {
          'now': GlitchDateTime(),
          'error_msg': self.request.get('error_msg')
        }
        d['now'].minutestr = "%02d" % d['now'].minute
        return d

    def go_home(self, msg=None):
        if msg:
            encoded = urlencode({'error_msg': msg})
            self.redirect('/?' + encoded)
        else:
            self.redirect('/')
