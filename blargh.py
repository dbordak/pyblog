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
    template = JINJA_ENVIRONMENT.get_template('templates/errors/404.html')
    response.write(template.render(template_values))


def handle500(request, response, exception):
    logging.exception(exception)
    template = JINJA_ENVIRONMENT.get_template('templates/errors/500.html')
    # Don't render anything in case it caused the 500
    response.write(template.render({}))


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
    def get(self, catsafe):
        template_values = genSidebar(users.get_current_user())

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

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class EntryPage(webapp2.RequestHandler):
    """Individual blog post page"""
    def get(self, year, month, title, entsafe):
        template_values = genSidebar(users.get_current_user())

        ent = ndb.Key(urlsafe=entsafe).get()
        if (str(ent.date.month) == month and str(ent.date.year) == year and
            ent.title_safe == title):
            template_values['title'] = ent.title
            template_values['content'] = ent.content

            template = JINJA_ENVIRONMENT.get_template('templates/entry.html')
            self.response.write(template.render(template_values))


class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = genSidebar(users.get_current_user())

        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route('/<year:\d{4}>/<month:\d{1,2}>/<title>/<entsafe>',
                  handler=EntryPage),
    webapp2.Route('/cat/<catsafe>', handler=CategoryPage),
    ('/about', AboutPage)
], debug=True)

application.error_handlers[404] = handle404
#application.error_handlers[500] = handle500
