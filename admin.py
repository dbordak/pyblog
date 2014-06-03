"""All administration pages."""

from os.path import dirname
from urllib import urlencode
from google.appengine.ext import ndb
import webapp2
import jinja2
import models
from blargh import handle404

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(__file__)))

class AddCategoryPage(webapp2.RequestHandler):
    """Administration panel for adding entries"""
    def get(self):
        template_values = {'cats': models.Category.query()}
        template = JINJA_ENVIRONMENT.get_template('templates/admin/add_cat.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request
        newCategory = models.Category()

        newCategory.name   = req.get('name')
        try:
            newCategory.parent = ndb.Key(urlsafe=req.get('parent'))
        except:
            pass
        newCategory.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class AddEntryPage(webapp2.RequestHandler):
    """Administration panel for adding entries"""
    def get(self):
        template_values = {'cats': models.Category.query()}
        template = JINJA_ENVIRONMENT.get_template('templates/admin/add_ent.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request
        newEntry = models.Entry()

        newEntry.title    = req.get('title')
        newEntry.content  = req.get('content')
        newEntry.category = ndb.Key(urlsafe=req.get('category'))
        newEntry.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class AdminNavPage(webapp2.RequestHandler):
    """Navigation page for administrative tasks."""
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/admin/nav.html')
        self.response.write(template.render({}))


application = webapp2.WSGIApplication([
    ('/admin/', AdminNavPage),
    ('/admin/add/ent', AddEntryPage),
    ('/admin/add/cat', AddCategoryPage),
], debug=True)

application.error_handlers[404] = handle404
