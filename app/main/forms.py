from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField


class SearchForm(Form):
    mate = StringField('what do you want?', validators=[Length(0, 64)])


class PostForm(Form):
    title = StringField('TITLE', validators=[DataRequired()])
    body = PageDownField('BODY', validators=[DataRequired()])
    summary = PageDownField('SUMMARY', validators=[DataRequired()])
    category = StringField('CATEGORY', validators=[DataRequired()])
    submit = SubmitField('post')


class EditForm(Form):
    title = StringField('TITLE', validators=[DataRequired()])
    body = PageDownField('BODY', validators=[DataRequired()])
    summary = PageDownField('SUMMARY', validators=[DataRequired()])
    submit = SubmitField('update')
