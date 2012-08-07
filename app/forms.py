"""
WTForms Documentation:    http://wtforms.simplecodes.com/
Flask WTForms Patterns:   http://flask.pocoo.org/docs/patterns/wtforms/
Flask-WTF Documentation:  http://packages.python.org/Flask-WTF/

Forms for your application can be stored in this file.
"""

from flaskext.wtf import BooleanField, Form, TextField, TextAreaField, \
    SubmitField, Required


class ArticleForm(Form):
    """Simple todo form."""
    title = TextField("Title", validators=[Required()])
    content = TextAreaField("Content", validators=[Required()])
    tags = TextField()
    is_public = BooleanField()
    submit = SubmitField("Create Article")

