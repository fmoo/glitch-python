from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from common import BaseHandler
from gaesessions import get_current_session

import logging

class MainPage(BaseHandler):
    def get(self):
        data = self.default_data()

        # Build data from session
        session = get_current_session()
        if session.is_active():
            data['has_token'] = True
            data['scope'] = session.get('oauth_scope')

        path = 'templates/home.html'
        self.response.out.write(template.render(path, data))


application = webapp.WSGIApplication([('/.*', MainPage)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
