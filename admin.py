"""All administration pages."""

from urllib import urlencode
from google.appengine.ext import ndb
import webapp2
import models
from blargh import handle404, JINJA_ENVIRONMENT

class AddCategoryPage(webapp2.RequestHandler):
    """Administration panel for adding categories"""
    def get(self):
        template_values = {'cats': models.Category.query()}
        template = JINJA_ENVIRONMENT.get_template('templates/admin/add_cat.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request
        newCategory = models.Category()

        newCategory.name = req.get('name')
        par = req.get('parent')
        if par != "":
            newCategory.parent = ndb.Key(urlsafe=par)
        newCategory.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))

# TODO: CSRF, Wap, rewrite with Kay
class DeleteCategoryPage(webapp2.RequestHandler):
    """Administration panel for deleting categories"""
    def get(self):
        template_values = {'cats': models.Category.query()}
        template = JINJA_ENVIRONMENT.get_template('templates/admin/del_cat.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request

        cat = req.get('category')
        if cat != "":
            ndb.Key(urlsafe=cat).delete()

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

        newEntry.title   = req.get('title')
        newEntry.content = req.get('content')
        cat = req.get('category')
        if cat != "":
            newEntry.category = ndb.Key(urlsafe=cat)
        newEntry.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class NavPage(webapp2.RequestHandler):
    """Navigation page for administrative tasks."""
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/admin/nav.html')
        self.response.write(template.render({}))


application = webapp2.WSGIApplication([
    ('/admin/', NavPage),
    ('/admin/add/ent', AddEntryPage),
    ('/admin/add/cat', AddCategoryPage),
    ('/admin/del/cat', DeleteCategoryPage),
], debug=True)

application.error_handlers[404] = handle404
