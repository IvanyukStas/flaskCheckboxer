from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from checkboxer import app, db
from flask import redirect, url_for, render_template, flash, request
from checkboxer.forms import UserForm, CheckboxlistForm, LoginForm, checkbox_list_form_builder
from checkboxer.models import User, Checkboxlist


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    add_user_form = UserForm()
    if add_user_form.validate_on_submit():
        user = User(user_name=add_user_form.user_name.data)
        user.set_password(add_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Пользователь {add_user_form.user_name.data} успешно добавлен в базу!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Чекбоксер', add_user_form=add_user_form)


@app.route('/add_checkbox_title', methods=['GET','POST'])
@login_required
def add_checkbox_title():
    add_checkbox_title = CheckboxlistForm()
    user = User.query.filter_by(user_name=current_user.user_name).first()
    if add_checkbox_title.validate_on_submit():
        checkbox_title = Checkboxlist(checkbox_list_title=add_checkbox_title.checkbox_list_title.data,
                                      checkbox_privacy=add_checkbox_title.checkbox_privacy.data,
                                      author=user)
        db.session.add(checkbox_title)
        db.session.commit()
        flash(f'Чекбокcвер с названием {checkbox_title.checkbox_list_title} успешно создан!')
        return redirect(url_for('index'))
    return render_template('add_checkboxer.html', title='Создать чекбоксер',
                           add_checkbox_title=add_checkbox_title,)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(user_name=login_form.login.data.lower()).first()
        if user is None or not user.check_assword(login_form.password.data):
            flash('Неверный логин или пароль!')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Станица входа', login_form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))