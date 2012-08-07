"""
Python Datastore API: http://code.google.com/appengine/docs/python/datastore/
"""

from google.appengine.ext import db


class Article(db.Model):
    number = db.IntegerProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    added = db.DateTimeProperty(auto_now_add=True)
    tags = db.StringProperty()
    is_public = db.BooleanProperty()

    def get_absolute_url(self):
        return "/a/%s/" % self.number
