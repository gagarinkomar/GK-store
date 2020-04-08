from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField, RadioField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия')
    about = TextAreaField('О себе')
    phone_number = StringField('Номер телефона')
    email = EmailField('Почта', validators=[DataRequired()])
    permission = SelectField('Роль', choices=[('seller', 'Продавец'),
                                              ('buyer', 'Покупатель')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
