from checkboxer import app, db
from flask import  redirect, url_for, render_template, flash
from checkboxer.forms import UserForm, CheckboxlistForm
from checkboxer.models import User, Checkboxlist


@app.route('/', methods=['GET','POST'])
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
def add_checkbox_title():
    add_checkbox_title = CheckboxlistForm()
    client = User.query.get(1)
    print(client)
    if add_checkbox_title.validate_on_submit():
        print(add_checkbox_title.checkbox_privacy.data)
        checkbox_title = Checkboxlist(checkbox_list_title=add_checkbox_title.checkbox_list_title.data,
                                      checkbox_privacy=add_checkbox_title.checkbox_privacy.data,
                                      author=client)
        db.session.add(checkbox_title)
        db.session.commit()
        flash(f'Чекбокcвер с названием {checkbox_title.checkbox_list_title} успешно создан!')
        return redirect(url_for('index'))
    return render_template('add_checkboxer.html', title='Создать чекбоксер', add_checkbox_title=add_checkbox_title)

