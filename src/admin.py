"""All administration pages."""

from urllib import urlencode
from google.appengine.ext import ndb
import webapp2
import models
import util

admin_template = lambda x: util.jinja_template('admin/' + x)


class AddCategoryPage(webapp2.RequestHandler):
    """Administration panel for adding categories"""
    def get(self):
        template_values = util.genSidebar()
        template = admin_template('add_cat')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request.get
        newCategory = models.Category()

        newCategory.name = req('name')
        if req('parent') != "":
            par = models.Category.get_by_id(int(req('parent')))
            if par.parent:
                # TODO: Warning that parent already has parent.
                pass
            else:
                newCategory.parent = par.key
        newCategory.put()

        query_params = {'blog': req('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


# TODO: CSRF, Wap, rewrite with Kay
class DeleteCategoryPage(webapp2.RequestHandler):
    """Administration panel for deleting categories"""
    def get(self):
        template_values = util.genSidebar()
        template = admin_template('del_cat')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request.get

        if req('category') != "":
            ndb.Key(models.Category, int(req('category'))).delete()

        query_params = {'blog': req('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class AddEntryPage(webapp2.RequestHandler):
    """Administration panel for adding entries"""
    def get(self):
        template_values = util.genSidebar()
        template = admin_template('add_ent')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request.get
        newEntry = models.Entry(
            title=req('title'),
            content=req('content')
        )

        if newEntry.title == "":
            newEntry.title = "Untitled"
        if req('category') != "":
            newEntry.category = ndb.Key(models.Category, int(req('category')))
        newEntry.put()

        query_params = {'blog': req('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class DeleteEntryPage(webapp2.RequestHandler):
    """Administration panel for deleting entries"""
    def get(self):
        template_values = util.genSidebar()
        template_values['ents'] = models.Entry.query()
        template = admin_template('del_ent')
        self.response.write(template.render(template_values))

    def post(self):
        req = self.request.get

        if req('entry') != "":
            ndb.Key(models.Entry, int(req('entry'))).delete()

        query_params = {'blog': req('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class NavPage(webapp2.RequestHandler):
    """Navigation page for administrative tasks."""
    def get(self):
        template_values = util.genSidebar()
        template = admin_template('nav')
        self.response.write(template.render(template_values))
