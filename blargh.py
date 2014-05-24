"""What will eventually be a blog."""

import os
import urllib
from google.appengine.ext import ndb  # Data modelling using DataStore
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class MainPage(webapp2.RequestHandler):
    """Display for blog entries"""
    def get(self):
        blog = self.request.get('blog', 'blog')
        entry_query = Entry.query(
            ancestor=entry_key(blog)).order(-Entry.date)
        entry_contents = (entry.content for entry in entry_query.fetch(10))

        template_values = {
            'template_test': r"</p><p>".join(entry_contents)
        }

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class Manage(webapp2.RequestHandler):
    """Administration panel for (adding? modifying?) entries"""
    def get(self):
        template_values = {
            'template_test': "You're the administrator!"
        }

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))

    def post(self):
        blog = self.request.get('blog', 'blog')
        newEntry = Entry(parent=entry_key('blog'))

        newEntry.title = self.request.get('title')
        newEntry.content = self.request.get('content')
        newEntry.put()

        query_params = {'blog': blog}
        self.redirect('/?' + urllib.urlencode(query_params))


class Entry(ndb.Model):
    """Models a blog entry"""
    title = ndb.StringProperty(indexed=False)  # Set index to True?
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    # tags?


def entry_key(blog_name='blog'):
    """Constructs a Datastore key for a blog entry"""
    return ndb.Key('Blog', blog_name)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin/', Manage)
], debug=True)
