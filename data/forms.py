from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField, SelectField, FloatField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия')
    about = TextAreaField('О себе')
    avatar_source = FileField('Аватарка')
    phone_number = StringField('Номер телефона')
    email = EmailField('Почта', validators=[DataRequired()])
    permission = SelectField('Роль', choices=[('seller', 'Продавец'),
                                              ('buyer', 'Покупатель')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProductForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    short_about = TextAreaField('Краткое описание', validators=[DataRequired()])
    about = TextAreaField('Описание', validators=[DataRequired()])
    image_source = FileField('Картинка')
    price = FloatField('Стоимость в рублях', validators=[DataRequired()])
    categories = StringField('Категории(через пробел)')
    purchased_content = TextAreaField('Купленная информация',
                                      validators=[DataRequired()])
    is_published = BooleanField('Видна неавторизированным пользователям')
    submit = SubmitField('Отправить на проверку')
