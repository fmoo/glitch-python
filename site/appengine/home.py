from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = 'templates/home.html'
        self.response.out.write(template.render(path, template_values))
        self.response.out.write('hello world')


application = webapp.WSGIApplication([('/.*', MainPage)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
