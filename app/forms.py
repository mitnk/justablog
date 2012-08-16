"""
WTForms Documentation:    http://wtforms.simplecodes.com/
Flask WTForms Patterns:   http://flask.pocoo.org/docs/patterns/wtforms/
Flask-WTF Documentation:  http://packages.python.org/Flask-WTF/

Forms for your application can be stored in this file.
"""

from flaskext.wtf import BooleanField, Form, TextField, TextAreaField, \
    SubmitField, Required


class ArticleForm(Form):
    title = TextField("Title", validators=[Required()])
    content = TextAreaField("Content", validators=[Required()])
    tags = TextField()
    is_public = BooleanField()
    submit = SubmitField("Create Article")


class SettingsForm(Form):
    blog_name = TextField("Blog Name", validators=[Required()])
    submit = SubmitField("Save")

