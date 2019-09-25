from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields.html5 import TelField

class RegisterForm(Form):
    first_name = StringField('first_name', validators=[DataRequired(), Length(min=6, max=40)])
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=6, max=40)])
    phone_number = TelField(validators=[DataRequired(), Length(min=10, max=15)])
    country_code = StringField('country_code', validators=[DataRequired(), Length(min=2, max=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(Form):
    phone_number = TelField(validators=[DataRequired(), Length(min=10, max=15)])
    country_code = StringField('country_code', validators=[DataRequired()])
