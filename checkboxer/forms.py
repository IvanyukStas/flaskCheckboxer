from wtforms import StringField, SelectField, SelectMultipleField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    user_name = StringField('User')
    password = PasswordField('Password', validators=[DataRequired()])
    submit1 = SubmitField('Добавить')


class CheckboxlistForm(FlaskForm):
    checkbox_list_title = StringField('Название чекбоксера')
    checkbox_privacy = BooleanField('Сделать чекбоксер публичным?')
    submit = SubmitField('Создать')
