"""What will eventually be a blog."""

from os.path import dirname
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import logging
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(__file__)))


def genSidebar(user=None):
    return {
        'isAdmin': user and users.is_current_user_admin(),
        'cats': models.Category.query()
    }


def handle404(request, response, exception):
    logging.exception(exception)
    template_values = genSidebar(users.get_current_user())
    template = JINJA_ENVIRONMENT.get_template('templates/404.html')
    response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    """List of blog entry summaries."""
    def get(self):
        template_values = genSidebar(users.get_current_user())
        entry_query = models.Entry.query().order(-models.Entry.date)
        template_values['entries'] = entry_query.fetch(10)

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class CategoryPage(webapp2.RequestHandler):
    """List of blog entry summaries for a given category."""
    def get(self, cat):
        template_values = genSidebar(users.get_current_user())
        entry_query = models.Entry.query(
            models.Entry.category == ndb.Key(urlsafe=cat)
        ).order(-models.Entry.date)
        template_values['entries'] = entry_query.fetch(10)

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = genSidebar(users.get_current_user())

        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    #('/(\d{4})/(\d{2})/', EntryPage),
    webapp2.Route('/cat/<cat>', handler=CategoryPage),
    ('/about', AboutPage)
], debug=True)

application.error_handlers[404] = handle404
