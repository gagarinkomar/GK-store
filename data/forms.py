from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField, SelectField, FloatField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=10)])
    surname = StringField('Фамилия', validators=[Length(max=20)])
    about = TextAreaField('О себе', validators=[Length(max=100)])
    avatar_source = FileField('Аватарка')
    phone_number = StringField('Номер телефона', validators=[Length(max=20)])
    email = EmailField('Почта', validators=[DataRequired(), Length(min=8, max=30)])
    permission = SelectField('Роль', choices=[('seller', 'Продавец'),
                                              ('buyer', 'Покупатель')])
    password_new = PasswordField('Пароль', validators=[DataRequired(), Length(min=5, max=35)])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class EditUserForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=10)])
    surname = StringField('Фамилия', validators=[Length(max=20)])
    about = TextAreaField('О себе', validators=[Length(max=100)])
    avatar_source = FileField('Аватарка')
    phone_number = StringField('Номер телефона', validators=[Length(max=20)])
    password_new = PasswordField('Новый пароль(не обязательно)', validators=[Length(max=35)])
    password_again = PasswordField('Повторите новый пароль')
    password = PasswordField('Пароль для принятия изменений', validators=[DataRequired()])
    submit = SubmitField('Изменить')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class ProductForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=10, max=50)])
    short_about = TextAreaField('Краткое описание', validators=[DataRequired(), Length(min=15, max=75)])
    about = TextAreaField('Полное описание', validators=[DataRequired(), Length(min=25, max=200)])
    image_source = FileField('Картинка')
    price = FloatField('Стоимость в рублях', validators=[DataRequired()])
    categories = StringField('Категории(через пробел)')
    purchased_content = TextAreaField('Купленная информация',
                                      validators=[DataRequired(), Length(min=10, max=100)])
    is_published = BooleanField('Видна неавторизированным пользователям')
    submit = SubmitField('Отправить на проверку')


class PromocodeForm(FlaskForm):
    promocode = StringField('Ввести промокод', validators=[DataRequired()])
    submit = SubmitField('Активировать')


class PromocodeCreateForm(FlaskForm):
    promocode = StringField('Добавить промокод', validators=[DataRequired()])
    award = FloatField(validators=[DataRequired()])
    submit = SubmitField('Добавить')


class SortingForm(FlaskForm):
    sorting = SelectField(choices=[('1', 'По дате добавления(раньше)'),
                                   ('2', 'По дате добавления(Позже)'),
                                   ('3', 'От дешёвых к дорогим'),
                                   ('4', 'От дорогих к дешёвым'),
                                   ('5', 'По отзывам')])
    submit = SubmitField('Сортировать')
