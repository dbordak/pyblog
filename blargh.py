"""What will eventually be a blog."""

from os.path import dirname
from urllib import urlencode
from google.appengine.api import users
import webapp2
import jinja2
from models import Entry, entry_key

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(__file__)))


def checkAdmin(blog, user=None):
    return {'isAdmin': user and users.is_current_user_admin()}


class MainPage(webapp2.RequestHandler):
    """List of blog entry summaries."""
    def get(self):
        blog = self.request.get('blog', 'blog')
        template_values = checkAdmin(blog, users.get_current_user())

        entry_query = Entry.query(ancestor=entry_key(blog)).order(-Entry.date)
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
        newEntry = Entry(parent=entry_key('blog'))

        newEntry.title    = req.get('title')
        newEntry.content  = req.get('content')
        newEntry.category = req.get('category')
        newEntry.subcat   = req.get('subcat')
        newEntry.put()

        query_params = {'blog': req.get('blog', 'blog')}
        self.redirect('/?' + urlencode(query_params))


class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = checkAdmin(self.request.get('blog', 'blog'),
                                     users.get_current_user())

        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage),
    #('/post/', EntryPage),
    #('/cat/', CategoryPage),
    ('/about', AboutPage)
], debug=True)
