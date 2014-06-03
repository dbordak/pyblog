from urllib import quote_plus
from google.appengine.ext import ndb


class Entry(ndb.Model):
    """Models a blog entry"""
    title = ndb.StringProperty('t', required=True)
    content = ndb.TextProperty('c', required=True)
    date = ndb.DateTimeProperty('d', auto_now_add=True, required=True)
    category = ndb.StringProperty('cat', required=True)
    subcat = ndb.StringProperty('sc', required=True)
    # tags = ndb.StringProperty(repeated=True)

    @property
    def url(self):
        return quote_plus(self.category + "/" + self.subcat + "/" + self.title)


def entry_key(blog_name='blog'):
    """Constructs a Datastore key for a blog entry"""
    return ndb.Key('Blog', blog_name)
