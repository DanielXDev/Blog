from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, ValidationError
import re

def validate_gmail(form, field):
    email = field.data.lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(pattern, email):
        raise ValidationError("Please use a valid Gmail address.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), validate_gmail])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), validate_gmail])
    name = StringField("Name", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")