from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import config
import requests
import logging
import monkeys

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        logging.error("json or simplejson are required to run this")
        raise

from urllib import urlencode


class OAuthIndex(webapp.RequestHandler):
    def get(self):
        scope = config.DEFAULT_SCOPE
        self.redirect('/oauth/' + scope + '/step1/')

class OAuthStep1(webapp.RequestHandler):
    def get(self, scope):
        # For Now, always redirect to glitch
        query = {
          'response_type': 'code',
          'client_id': config.APIKEY,
          'redirect_uri': config.REDIRECT_URI,
          'scope': scope,
          #'state': 'wtf',
        }
        encoded = urlencode(query)
        self.redirect('http://api.glitch.com/oauth2/authorize?' + encoded)


import pprint
class OAuthStep2(webapp.RequestHandler):
    def oauth_fail(self, obj):
        self.error(400)
        description = obj.get('error_description', None)

        # XXX- Do something smarter than just printing this error message
        if description is not None:
            self.response.out.write(description)

    def get(self):
        code = self.request.get('code', None)
        if code is None:
            self.oauth_fail(self.request)
            return

        # Now get the Access Token
        query = {
          'grant_type': 'authorization_code',
          'code': code,
          'client_id': config.APIKEY,
          'client_secret': config.SECRET,

          # Why do we need this?
          'redirect_uri': config.REDIRECT_URI,
        }
        encoded = urlencode(query)

        resp = requests.post('http://api.glitch.com/oauth2/token', encoded)
        data = json.loads(resp.content)

        # Make sure the response was valid
        if data.get('error', None) is not None:
            self.oauth_fail(data)
            return

        # There's should be some junk in this data dictionary:
        # - 'access_token' - Save this somewhere
        # - 'token_type' - I get 'bearer' pretty much all the time;
        #                  must be some kind of spec compliance thing
        # - 'scope' - should match the scope you sent in stage1
        self.response.out.write("It Worked")

        # XXX- Hey, you should save data['access_token'] for this user


application = webapp.WSGIApplication([('/oauth/', OAuthIndex),
                                      ('/oauth/(\w+)/step1/', OAuthStep1),
                                      ('/oauth/step2/', OAuthStep2)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
