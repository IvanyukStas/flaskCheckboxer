from wtforms import StringField, SelectField, SelectMultipleField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    user_name = StringField('User')
    password = PasswordField('Password', validators=[DataRequired()])
    submit1 = SubmitField('Добавить')