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
        if self.is_public:
            return "/a/%s/" % self.number
        else:
            return "/p/%s/" % self.number

    def get_edit_url(self):
        return "/edit/%s/" % self.number


class Comment(db.Model):
    article_number = db.IntegerProperty(required=True)
    author = db.StringProperty(required=True)
    comment = db.TextProperty(required=True)
    added = db.DateTimeProperty(auto_now_add=True)

