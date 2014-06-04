"""What will eventually be a blog."""

from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
import webapp2
import models
import util


def getPage(query, req):
    curs = Cursor(urlsafe=req.get('cursor'))
    entries, next_curs, more = query.fetch_page(10, start_cursor=curs)

    button = next_curs.urlsafe() if more and next_curs else None
    return (entries, button)


class MainPage(webapp2.RequestHandler):
    """List of blog entry summaries."""
    def get(self):
        template_values = util.genSidebar(users.get_current_user())
        entry_query = models.Entry.query().order(-models.Entry.date)

        template_values['entries'], template_values['next_button'] = getPage(
            entry_query, self.request)

        template = util.jinja_template('index')
        self.response.write(template.render(template_values))


class CategoryPage(webapp2.RequestHandler):
    """List of blog entry summaries for a given category, plus any
    child categories."""
    def get(self, catid):
        template_values = util.genSidebar(users.get_current_user())
        cat = models.Category.get_by_id(int(catid))

        # Find all child categories when we're looking at a parentless key.
        subcats = models.Category.query(
            models.Category.parent == cat.key
        ).fetch(keys_only=True) if (cat.parent is None) else []
        # ...Plus the key itself.
        subcats.append(cat.key)

        entry_query = models.Entry.query(
            models.Entry.category.IN(subcats)
        ).order(-models.Entry.date)

        template_values['entries'], template_values['next_button'] = getPage(
            entry_query, self.request)

        template = util.jinja_template('index')
        self.response.write(template.render(template_values))


class EntryPage(webapp2.RequestHandler):
    """Individual blog post page"""
    def get(self, year, month, title, entid):
        template_values = util.genSidebar(users.get_current_user())
        ent = models.Entry.get_by_id(int(entid))

        # TODO: Make this look nicer
        if (
            str(ent.date.month) == month and str(ent.date.year) == year
            and ent.title_safe == title
        ):
            template_values['title'] = ent.title
            template_values['content'] = ent.content

            template = util.jinja_template('entry')
            self.response.write(template.render(template_values))
        else:
            return webapp2.redirect(ent.url, permanent=True)


class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = util.genSidebar(users.get_current_user())

        template = util.jinja_template('about')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route('/<year:\d{4}>/<month:\d{1,2}>/<title>/<entid>',
                  handler=EntryPage),
    webapp2.Route('/cat/<catid>', handler=CategoryPage),
    ('/about', AboutPage)
], debug=True)

application.error_handlers[404] = util.handle404
# application.error_handlers[500] = util.handle500
