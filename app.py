import os
from flask import Flask, render_template, redirect, abort, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user,\
    current_user
from flask_uploads import configure_uploads, IMAGES, UploadSet
import datetime

from data import db_session
from data.users import User
from data.products import Product
from data.categories import Category
from data.transactions import Transaction
from data.forms import RegisterForm, LoginForm, ProductForm, EditUserForm



app = Flask(__name__)
app.config['SECRET_KEY'] = '474B70726F64756374696F6E5F3533637233375F6B3379'
app.config['UPLOADED_IMAGES_DEST'] = os.path.join('static', 'img')
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


@app.route('/', methods=['GET', 'POST'])
def index():
    choosed_categories = set()
    if request.method == 'POST':
        choosed_categories = set(request.form.getlist('categories_checkbox'))
    session = db_session.create_session()
    products = session.query(Product).filter(Product.is_checked, Product.is_sold != True).all()
    products = [
        (product, url_for('static', filename=f'img/{product.image_source}'))
        for product in filter(lambda x: choosed_categories <= set(
            map(lambda y: y.name, x.categories)), products)]
    categories = session.query(Category).all()
    return render_template('index.html', products=products, categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password_new.data != form.password_again.data:
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
            user.avatar_source = images.save(form.avatar_source.data)
        user.set_password(form.password_new.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    email, permission = None, None
    form = EditUserForm()
    if request.method == "GET":
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.about.data = user.about
            form.avatar_source.data = user.avatar_source
            form.phone_number.data = user.phone_number
            email = user.email
            permission = user.permission
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.id == current_user.id).first()
        if user:
            if not user.check_password(form.password.data):
                email = user.email
                permission = user.permission
                return render_template('register.html',
                                       title='Редактирование пользователя',
                                       email=email, form=form,
                                       permission=permission,
                                       message='Неверный пароль')
            if form.password_new.data != form.password_again.data:
                email = user.email
                permission = user.permission
                return render_template('register.html',
                                       title='Редактирование пользователя',
                                       email=email, form=form,
                                       permission=permission,
                                       message='Пароли не совпадают')
            user.name = form.name.data
            user.phone_number = form.phone_number.data
            user.about = form.about.data
            user.surname = form.surname.data
            if form.avatar_source.data.filename:
                user.avatar_source = images.save(form.avatar_source.data)
            if form.password_new.data:
                user.set_password(form.password_new.data)
                user.last_changed_date = datetime.datetime.now()
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('register.html', title='Редактирование пользователя', email=email, form=form, permission=permission)


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
        product = Product(
            user_id=current_user.id,
            title=form.title.data,
            short_about=form.short_about.data,
            about=form.about.data,
            price=form.price.data,
            purchased_content=form.purchased_content.data,
            is_published=form.is_published.data
        )
        if form.image_source.data.filename:
            product.image_source = images.save(form.image_source.data)
        for category_name in form.categories.data.lower().split(' '):
            if category_name not in map(lambda x: x.name, session.query(Category).all()):
                category = Category(name=category_name)
                session.add(category)
                session.commit()
            product.categories.append(session.query(Category).filter(Category.name == category_name).first())
        session.add(product)
        session.commit()
        return redirect('/')
    return render_template('product.html', title='Добавить товар', form=form)


@app.route('/product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.permission != 'seller':
        abort(403)
    form = ProductForm()
    if request.method == "GET":
        session = db_session.create_session()
        product = session.query(Product).filter(
            Product.id == id, Product.user == current_user).first()
        if product:
            form.title.data = product.title
            form.short_about.data = product.short_about
            form.about.data = product.about
            form.price.data = product.price
            form.purchased_content.data = product.purchased_content
            form.is_published.data = product.is_published
            form.categories.data = ', '.join(map(lambda x: x.name,
                                                 product.categories))
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        product = session.query(Product).filter(
            Product.id == id, Product.user == current_user).first()
        if product:
            product.title = form.title.data
            product.short_about = form.short_about.data
            product.about = form.about.data
            product.price = form.price.data
            form.purchased_content = form.purchased_content.data
            product.is_checked = False
            if form.image_source.data.filename:
                product.image_source = images.save(form.image_source.data)
            for category in product.categories:
                product.categories.remove(category)
            print(len(product.categories))
            for category_name in form.categories.data.lower().split(', '):
                if category_name not in map(lambda x: x.name,
                                            session.query(Category).all()):
                    category = Category(name=category_name)
                    session.add(category)
                    session.commit()
                product.categories.append(session.query(Category).filter(
                    Category.name == category_name).first())
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('product.html', title='Редактирование товара',
                           form=form)


@app.route('/user_about/<int:id>')
@login_required
def user_about(id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if not user:
        abort(404)
    if user.permission == 'admin' and current_user.permission != 'admin':
        abort(403)
    user_avatar_source = url_for('static', filename=f'img/{user.avatar_source}')
    products = session.query(Product).filter(Product.is_checked, Product.user_id == id).all()
    products = [(product, url_for('static', filename=f'img/{product.image_source}'))for product in products]
    return render_template('user_about.html', user=user, user_avatar_source=user_avatar_source, products=products)


@app.route('/product_about/<int:id>', methods=['GET', 'POST'])
@login_required
def product_about(id):
    session = db_session.create_session()
    product = session.query(Product).filter(Product.id == id).first()
    if not product:
        abort(404)
    if not product.is_checked and not current_user.permission == 'admin':
        abort(403)
    if request.method == 'POST':
        product.is_checked = True
        session.commit()
        return redirect('../products_check')
    product_image_source = url_for('static', filename=f'img/{product.image_source}')
    return render_template('product_about.html', product=product, product_image_source=product_image_source)


@app.route('/transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def transaction(id):
    session = db_session.create_session()
    product = session.query(Product).filter(Product.id == id).first()
    if not product.is_checked or product.is_sold:
        abort(404)
    if request.method == 'POST':
        user = session.query(User).filter(User.id == current_user.id).first()
        admin = session.query(User).filter(User.permission == 'admin').first()
        transaction = Transaction()
        transaction.seller_id = product.user_id
        transaction.buyer_id = current_user.id
        transaction.product_id = product.id
        transaction.status = 'Куплено'
        product.is_sold = True
        user.balance -= product.price
        product.user.balance += product.price * 0.95
        admin.balance += product.price * 0.05
        transaction.price = product.price
        session.add(transaction)
        session.commit()
        return redirect(f'/transaction_about/{transaction.id}')
    return render_template('transaction.html', product=product)


@app.route('/transactions/')
@login_required
def transactions():
    session = db_session.create_session()
    if current_user.permission == 'admin':
        transactions = session.query(Transaction).all()
    else:
        transactions = session.query(Transaction).filter((Transaction.buyer_id == current_user.id) | (Transaction.seller_id == current_user.id))
    return render_template('transactions.html', transactions=transactions)


@app.route('/transaction_about/<int:id>')
@login_required
def transaction_about(id):
    session = db_session.create_session()
    transaction = session.query(Transaction).filter(Transaction.id == id).first()
    if not transaction:
        abort(404)
    if transaction.buyer_id != current_user.id and transaction.seller_id != current_user.id and current_user.permission != 'admin':
        abort(403)
    product = transaction.product
    return render_template('transaction.html', product=product)


@app.route('/balance')
@login_required
def balance(id):
    return 123


@app.route('/products_check')
@login_required
def products_check():
    session = db_session.create_session()
    products = session.query(Product).filter(Product.is_checked != True).all()
    products = [
        (product, url_for('static', filename=f'img/{product.image_source}'))
        for product in products]
    return render_template('index.html', products=products)



def main():
    db_session.global_init('db/GK-store.sqlite')

    app.run(debug=True)


if __name__ == '__main__':
    main()
