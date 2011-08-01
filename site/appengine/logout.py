from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from common import BaseHandler

import config
import logging


class LogoutHandler(BaseHandler):
    def get(self):
        session = get_current_session()
        if session.is_active():
            session.terminate()
        self.go_home()


application = webapp.WSGIApplication([('/logout/', LogoutHandler)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
