from wtforms import StringField, SelectField, SelectMultipleField, PasswordField, SubmitField, BooleanField, FieldList, \
    FormField, ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from checkboxer.models import User


class UserForm(FlaskForm):
    user_name = StringField('User')
    password = PasswordField('Password', validators=[DataRequired()])
    submit1 = SubmitField('Добавить')


class CheckboxlistForm(FlaskForm):
    checkbox_list_title = StringField('Название чекбоксера')
    checkbox_privacy = BooleanField('Сделать чекбоксер публичным?')
    submit = SubmitField('Создать')


class CheckboxForm(FlaskForm):
    checkbox = StringField('Название чекбокса')
    submit_add = SubmitField('Создать')




class LoginForm(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

    def validate_username(self, login):
        user = User.query.filter_by(user_name=login)
        if not user:
            raise ValidationError('неверный логин!')


def checkbox_list_form_builder(filenames):
    class CheckboxListForm(FlaskForm):
        pass
    for (i, filename) in enumerate(filenames):
        setattr(CheckboxListForm, f'{filename.id}', BooleanField(label=filename.checkbox_name,
                                                        default=filename.checkbox_status,
                                                         false_values=('False', 'false', '')))
    setattr(CheckboxListForm, 'submit_write_checkbox_status', SubmitField('Записать'))
    return CheckboxListForm()