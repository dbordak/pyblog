"""What will eventually be a blog."""

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import models
import util


class MainPage(webapp2.RequestHandler):
    """List of blog entry summaries."""
    def get(self):
        template_values = util.genSidebar(users.get_current_user())
        entry_query = models.Entry.query().order(-models.Entry.date)
        template_values['entries'] = entry_query.fetch(10)

        template = util.jinja_template('templates/index.html')
        self.response.write(template.render(template_values))


class CategoryPage(webapp2.RequestHandler):
    """List of blog entry summaries for a given category."""
    def get(self, catsafe):
        template_values = util.genSidebar(users.get_current_user())

        catk = ndb.Key(urlsafe=catsafe)
        cat = catk.get()
        subcats = [
            sc.key for sc in models.Category.query(
                models.Category.parent == catk
            ).fetch()
        ] if cat.parent == None else []
        subcats.append(catk)
        entry_query = models.Entry.query(
            models.Entry.category.IN(subcats)
        ).order(-models.Entry.date)
        template_values['entries'] = entry_query.fetch(10)

        template = util.jinja_template('templates/index.html')
        self.response.write(template.render(template_values))


class EntryPage(webapp2.RequestHandler):
    """Individual blog post page"""
    def get(self, year, month, title, entsafe):
        template_values = util.genSidebar(users.get_current_user())

        ent = ndb.Key(urlsafe=entsafe).get()
        if (str(ent.date.month) == month and str(ent.date.year) == year and
            ent.title_safe == title):
            template_values['title'] = ent.title
            template_values['content'] = ent.content

            template = util.jinja_template('templates/entry.html')
            self.response.write(template.render(template_values))
        else:
            return webapp2.redirect(ent.url, permanent=True)

class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = util.genSidebar(users.get_current_user())

        template = util.jinja_template('templates/about.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route('/<year:\d{4}>/<month:\d{1,2}>/<title>/<entsafe>',
                  handler=EntryPage),
    webapp2.Route('/cat/<catsafe>', handler=CategoryPage),
    ('/about', AboutPage)
], debug=True)

application.error_handlers[404] = util.handle404
#application.error_handlers[500] = util.handle500
