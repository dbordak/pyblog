"""All administration pages."""

from urllib import urlencode
from google.appengine.ext import ndb
import webapp2
import models
import util


class AddCategoryPage(webapp2.RequestHandler):
    """Administration panel for adding categories"""
    def get(self):
        template_values = util.genSidebar()
        template = util.jinja_template('templates/admin/add_cat.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request
        newCategory = models.Category()

        newCategory.name = req.get('name')
        parsafe = req.get('parent')
        if parsafe != "":
            park = ndb.Key(urlsafe=parsafe)
            if park.get().parent:
                # TODO: Warning that parent already has parent.
                pass
            else:
                newCategory.parent = park
        newCategory.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


# TODO: CSRF, Wap, rewrite with Kay
class DeleteCategoryPage(webapp2.RequestHandler):
    """Administration panel for deleting categories"""
    def get(self):
        template_values = util.genSidebar()
        template = util.jinja_template('templates/admin/del_cat.html')
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
        template_values = util.genSidebar()
        template = util.jinja_template('templates/admin/add_ent.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request
        newEntry = models.Entry()

        newEntry.title = req.get('title')
        if newEntry.title == "":
            newEntry.title = "Untitled"
        newEntry.content = req.get('content')
        cat = req.get('category')
        if cat != "":
            newEntry.category = ndb.Key(urlsafe=cat)
        newEntry.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class DeleteEntryPage(webapp2.RequestHandler):
    """Administration panel for deleting entries"""
    def get(self):
        template_values = util.genSidebar()
        template_values['ents'] = models.Entry.query()
        template = util.jinja_template('templates/admin/del_ent.html')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request

        ent = req.get('entry')
        if ent != "":
            ndb.Key(urlsafe=ent).delete()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class NavPage(webapp2.RequestHandler):
    """Navigation page for administrative tasks."""
    def get(self):
        template_values = util.genSidebar()
        template = util.jinja_template('templates/admin/nav.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/admin/', NavPage),
    ('/admin/add/ent', AddEntryPage),
    ('/admin/del/ent', DeleteEntryPage),
    ('/admin/add/cat', AddCategoryPage),
    ('/admin/del/cat', DeleteCategoryPage),
], debug=True)

application.error_handlers[404] = util.handle404
# application.error_handlers[500] = util.handle500
