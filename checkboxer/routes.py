from checkboxer import app, db
from flask import  redirect, url_for, render_template, flash
from checkboxer.forms import UserForm
from checkboxer.models import User


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
