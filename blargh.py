"""What will eventually be a blog."""

from os.path import dirname
from urllib import urlencode
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import logging
import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(__file__)))


def checkAdmin(user=None):
    return {'isAdmin': user and users.is_current_user_admin()}


def handle404(request, response, exception):
    logging.exception(exception)
    template_values = checkAdmin(users.get_current_user())
    template = JINJA_ENVIRONMENT.get_template('templates/404.html')
    response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    """List of blog entry summaries."""
    def get(self):
        blog = self.request.get('blog', 'blog')
        template_values = checkAdmin(users.get_current_user())

        entry_query = models.Entry.query().order(-models.Entry.date)
        template_values['entries'] = entry_query.fetch(10)

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class AdminPage(webapp2.RequestHandler):
    """Administration panel for (adding? modifying?) entries"""
    def get(self):
        # template_values = checkAdmin(self.request.get('blog', 'blog'))
        template = JINJA_ENVIRONMENT.get_template('templates/admin.html')
        self.response.write(template.render({}))

    def post(self):
        req = self.request
        newEntry = models.Entry()

        newEntry.title    = req.get('title')
        newEntry.content  = req.get('content')
        newEntry.category = req.get('category')
        newEntry.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = checkAdmin(users.get_current_user())

        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin/add', AdminPage),
    #('/post/', EntryPage),
    #('/cat/', CategoryPage),
    ('/about', AboutPage)
], debug=True)

application.error_handlers[404] = handle404
