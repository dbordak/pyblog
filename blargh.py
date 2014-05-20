"""What will eventually be a blog."""

import os
from google.appengine.ext import ndb  # Data modelling using DataStore
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'template_test': "This is a test of Jinja2."
        }

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


class Post(ndb.Model):
    """Models a blog post"""
    title = ndb.StringProperty(indexed=False)  # Set index to True?
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    # tags?


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
