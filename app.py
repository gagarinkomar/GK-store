import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user,\
    current_user
from flask_uploads import configure_uploads, IMAGES, UploadSet

from data import db_session
from data.users import User
from data.products import Product
from data.categories import Category
from data.forms import RegisterForm, LoginForm, ProductForm



app = Flask(__name__)
app.config['SECRET_KEY'] = '474B70726F64756374696F6E5F3533637233375F6B3379'
app.config['UPLOADED_IMAGES_DEST'] = os.path.join('uploads', 'img')
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['png', 'jpg', 'jpeg'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)


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
        if form.avatar_source.data.filename:
            user.avatar_source = os.path.join(
                'uploads', 'img', images.save(
                    form.avatar_source.data))
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.permission != 'seller':
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = Product(
            user_id=current_user.id,
            title=form.title.data,
            about=form.about.data,
            price=form.price.data,
            purchased_content=form.purchased_content.data,
            is_published=form.is_published.data
        )
        if form.image_source.data.filename:
            user.image_source = os.path.join(
                'uploads', 'img', images.save(
                    form.image_source.data))
        for category_name in form.categories.data.lower().split(', '):
            if category_name not in map(lambda x: x.name, session.query(Category).all()):
                category = Category(name=category_name)
                session.add(category)
                session.commit()
            user.categories.append(session.query(Category).filter(Category.name == category_name).first())
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('product.html', title='Добавить товар', form=form)


def main():
    db_session.global_init('db/GK-store.sqlite')

    app.run(debug=True)


if __name__ == '__main__':
    main()
