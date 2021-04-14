

from flask_json import json_response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from checkboxer import app, db, json
from sqlalchemy import desc
from flask import redirect, url_for, render_template, flash, request, jsonify
from checkboxer.forms import UserForm, CheckboxlistForm, LoginForm, checkbox_list_form_builder, CheckboxForm
from checkboxer.models import User, Checkboxlist, Checkbox


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    add_user_form = UserForm()
    checkboxers = Checkboxlist.query.filter_by(user_id=current_user.id).order_by(desc(Checkboxlist.checkbox_list_title)).all()
    if add_user_form.validate_on_submit():
        user = User(user_name=add_user_form.user_name.data)
        user.set_password(add_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Пользователь {add_user_form.user_name.data} успешно добавлен в базу!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Чекбоксер', add_user_form=add_user_form,
                           checkboxers=checkboxers)


@app.route('/add_checkbox_title', methods=['GET', 'POST'])
@login_required
def add_checkbox_title():
    add_checkbox_title = CheckboxlistForm()
    user = User.query.filter_by(user_name=current_user.user_name).first()
    if add_checkbox_title.validate_on_submit():
        print('ХУЯЧУ')
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


@app.route('/checkboxer/<checkboxer>/<int:id>', methods=['GET', 'POST'])
def checkboxer(checkboxer, id):
    add_checkbox = CheckboxForm()
    checkboxer = Checkboxlist.query.get(id)
    get_checkbox_for_dynamic_build = Checkbox.query.filter_by(checkbox_list=id).order_by(Checkbox.checkbox_status).all()
    if get_checkbox_for_dynamic_build:
        dynamic_checkbox_builder = checkbox_list_form_builder(get_checkbox_for_dynamic_build)
    else:
        dynamic_checkbox_builder = None
    if add_checkbox.validate_on_submit() and add_checkbox.submit_add.data:
        if not add_checkbox.checkbox.data:
            flash('Заполните название чекбокса!!!')
            return redirect(url_for('checkboxer', checkboxer=checkboxer.checkbox_list_title,
                                    id=checkboxer.id))
        checkbox = Checkbox(checkbox_name=add_checkbox.checkbox.data, user_checkboxer=checkboxer)
        db.session.add(checkbox)
        db.session.commit()
        flash('Добавили новый чекбокс в чекбоксер!')
        return redirect(url_for('checkboxer', checkboxer=checkboxer.checkbox_list_title,
                                id=checkboxer.id))
    return render_template('checkbox.html', title='Чекбоксы', add_checkbox=add_checkbox,
                           dynamic_checkbox_builder=dynamic_checkbox_builder,
                           checkboxer=checkboxer)

@app.route('/js', methods=['GET','POST'])

def js():
    data = request.get_json(force=True)
    checkbox = Checkbox.query.filter_by(id=data['id']).first()
    checkbox.checkbox_status = data['instanse']
    db.session.add(checkbox)
    db.session.commit()
    a = {'id':'1', 'instanse':'False'}
    return json_response(data_=a)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@json.error_handler
def error_handler(e):
    # e - JsonError.
    return render_template('404.html')