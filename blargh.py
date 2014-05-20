"""What will eventually be a blog."""

from google.appengine.ext import ndb  # Data modelling using DataStore
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


class Post(ndb.Model):
    """Models a blog post"""
    title = ndb.StringProperty(indexed=False)  # Set index to True?
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    # tags?


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
