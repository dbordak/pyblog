"""What will eventually be a blog."""

import os
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def genSidebar(blog, user=None):
    """Generate the contents of the navigation sidebar."""
    entry_query = Entry.query(ancestor=entry_key(blog)).order(-Entry.date)
    entries = entry_query.fetch(10)
    line = ['<a href=/"' + entry.title + '"/>' + entry.title + "</a>"
            for entry in entries]
    if user and users.is_current_user_admin():
        line.append('<br><a href="/admin/" />Admin Page</a>')
    return "<br>".join(line)


class MainPage(webapp2.RequestHandler):
    """Display for blog entries"""
    def get(self):
        entry_list = genSidebar(self.request.get('blog', 'blog'),
                                users.get_current_user())
        template_values = {
            'heading': "Main Page",
            'body': "This is the main page of a blog.",
            'entry_list': entry_list
        }

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class Manage(webapp2.RequestHandler):
    """Administration panel for (adding? modifying?) entries"""
    def get(self):
        entry_list = genSidebar(self.request.get('blog', 'blog'))
        template_values = {
            'heading': "Administation",
            'body': "This is the administration page. Post a post with a POST"
            + " to this URL to post that post onto the blog, posthaste!",
            'entry_list': entry_list
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
