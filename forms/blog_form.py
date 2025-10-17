from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL

class CreateBlogForm(FlaskForm):
    title = StringField("Blog Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    body = TextAreaField("Blog Content", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit Post")