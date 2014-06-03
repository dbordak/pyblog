from urllib import quote_plus
from google.appengine.ext import ndb


class Category(ndb.Model):
    name = ndb.StringProperty('n', required=True)
    parent = ndb.KeyProperty('p', kind='Category')
    parent = ndb.KeyProperty('p')


class Entry(ndb.Model):
    """Models a blog entry"""
    title = ndb.StringProperty('t', required=True, indexed=False)
    content = ndb.TextProperty('c', required=True)
    date = ndb.DateTimeProperty('d', auto_now_add=True, required=True)
    category = ndb.KeyProperty('cat', kind='Category')

    # @property
    # def url(self):
    #     return self.date.year + "/" + self.date.month + "/" + self.date.day
    #     + "/" + quote_plus(self.title) + "-" + self.key.id()
