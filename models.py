from urllib import quote_plus
from google.appengine.ext import ndb


class Category(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    entries = ndb.StructuredProperty(Entry, 'e', repeated=True)


class SubCategory(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    entries = ndb.KeyProperty('e', kind=Entry, repeated=True)
    parent = ndb.KeyProperty('p', kind=Category)


class Entry(ndb.Model):
    """Models a blog entry"""
    title = ndb.StringProperty('t', required=True)
    content = ndb.TextProperty('c', required=True)
    date = ndb.DateTimeProperty('d', auto_now_add=True, required=True)
    category = ndb.KeyProperty('cat', kind=Category)
    subcat = ndb.KeyProperty('sc', kind=SubCategory)

    @property
    def url(self):
        return quote_plus(self.category + "/" + self.subcat + "/" + self.title)


def entry_key(blog_name='blog'):
    """Constructs a Datastore key for a blog entry"""
    return ndb.Key('Blog', blog_name)
