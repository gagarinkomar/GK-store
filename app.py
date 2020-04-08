from flask import Flask, render_template, redirect
from flask_login import LoginManager

from data import db_session
from data.users import User
from data.products import Product
from data.categories import Category
from data.forms import RegisterForm



app = Flask(__name__)
app.config['SECRET_KEY'] = '474B70726F64756374696F6E5F3533637233375F6B3379'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            permission=form.permission.data,
        )
        if form.phone_number.data:
            user.phone_number = form.phone_number.data
        if form.about.data:
            user.about = form.about.data
        if form.surname.data:
            user.surname = form.surname.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init('db/GK-store.sqlite')

    app.run(debug=True)


if __name__ == '__main__':
    main()
