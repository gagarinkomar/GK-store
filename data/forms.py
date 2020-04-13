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
    password_new = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class EditUserForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия')
    about = TextAreaField('О себе')
    avatar_source = FileField('Аватарка')
    phone_number = StringField('Номер телефона')
    password_new = PasswordField('Новый пароль(не обязательно)')
    password_again = PasswordField('Повторите новый пароль')
    password = PasswordField('Пароль для принятия изменений', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProductForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    short_about = TextAreaField('Краткое описание', validators=[DataRequired()])
    about = TextAreaField('Полное описание', validators=[DataRequired()])
    image_source = FileField('Картинка')
    price = FloatField('Стоимость в рублях', validators=[DataRequired()])
    categories = StringField('Категории(через пробел)')
    purchased_content = TextAreaField('Купленная информация',
                                      validators=[DataRequired()])
    is_published = BooleanField('Видна неавторизированным пользователям')
    submit = SubmitField('Отправить на проверку')
