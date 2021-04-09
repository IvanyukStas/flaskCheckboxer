from wtforms import StringField, SelectField, SelectMultipleField, PasswordField, SubmitField, BooleanField, FieldList, \
    FormField
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


class LoginForm(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')


def checkbox_list_form_builder(filenames):
    class CheckboxListForm(FlaskForm):

        submit = SubmitField('Записать')

    for (i, filename) in enumerate(filenames):
        setattr(CheckboxListForm, 'filename_%d' % i, BooleanField(label=filename.checkbox_list_title))

    return CheckboxListForm()