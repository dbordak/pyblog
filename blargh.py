"""What will eventually be a blog."""

import os
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users
import webapp2
import jinja2

CATEGORIES = ('example', 'fruit', 'programming', 'headwear', 'music')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


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
        self.redirect('/?' + urllib.urlencode(query_params))


class AboutPage(webapp2.RequestHandler):
    """About me page"""
    def get(self):
        template_values = checkAdmin(self.request.get('blog', 'blog'),
                                     users.get_current_user())

        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render(template_values))


class Entry(ndb.Model):
    """Models a blog entry"""
    title = ndb.StringProperty('t', required=True)
    content = ndb.TextProperty('c', required=True)
    date = ndb.DateTimeProperty('d', auto_now_add=True, required=True)
    category = ndb.StringProperty('cat', required=True, choices=CATEGORIES)
    subcat = ndb.StringProperty('sc', required=True)
    # tags = ndb.StringProperty(repeated=True)

    @property
    def url(self):
        return urllib.quote_plus(self.category + "/" + self.subcat + "/" +
                                 self.title)


def entry_key(blog_name='blog'):
    """Constructs a Datastore key for a blog entry"""
    return ndb.Key('Blog', blog_name)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage),
    #('/post/', EntryPage),
    #('/cat/', CategoryPage),
    ('/about', AboutPage)
], debug=True)
