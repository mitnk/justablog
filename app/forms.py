"""
WTForms Documentation:    http://wtforms.simplecodes.com/
Flask WTForms Patterns:   http://flask.pocoo.org/docs/patterns/wtforms/
Flask-WTF Documentation:  http://packages.python.org/Flask-WTF/

Forms for your application can be stored in this file.
"""

from flaskext.wtf import BooleanField, Form, TextField, TextAreaField, \
    SubmitField, Required, HiddenField


class ArticleForm(Form):
    title = TextField("Title", validators=[Required()])
    content = TextAreaField("Content", validators=[Required()])
    tags = TextField()
    is_public = BooleanField()
    submit = SubmitField("Create Article")


class CommentForm(Form):
    article_number = HiddenField("Article Number")
    author = TextField("Your Name", validators=[Required()])
    checker = TextField("Input the number of this month", validators=[Required()])
    comment = TextAreaField("Your Comment", validators=[Required()])
    submit = SubmitField("Add a Comment")


class SettingsForm(Form):
    blog_name = TextField("Blog Name", validators=[Required()])
    submit = SubmitField("Save")

