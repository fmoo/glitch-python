from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from common import BaseHandler

import config
import requests
import logging
import monkeys

from glitch.compat import json
from urllib import urlencode


class OAuthIndex(BaseHandler):
    def get(self):
        scope = config.DEFAULT_SCOPE
        self.redirect('/oauth/' + scope + '/step1/')

class OAuthStep1(BaseHandler):
    def get(self, scope):
        session = get_current_session()
        if session.is_active():
            if session.get('scope') == scope:
                self.go_home('You\'re already authenticated!')
                return

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
class OAuthStep2(BaseHandler):
    def oauth_fail(self, obj):
        self.error(400)
        description = obj.get('error_description', None)

        if description is not None:
            self.go_home(description)
            return

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
        session = get_current_session()
        session.start()
        if not session.is_active():
            self.go_home('It worked, but you need a session to continue')
            return

        session['oauth_access_token'] = data.get('access_token')
        session['oauth_scope'] = data.get('scope')
        session['ouath_token_type'] = data.get('token_type')
        self.go_home()

        # XXX- Hey, you should save data['access_token'] for this user


application = webapp.WSGIApplication([('/oauth/', OAuthIndex),
                                      ('/oauth/(\w+)/step1/', OAuthStep1),
                                      ('/oauth/step2/', OAuthStep2)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
