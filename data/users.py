import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String, default='')
    about = sqlalchemy.Column(sqlalchemy.String,
                              default='Информация отсутствует.')
    phone_number = sqlalchemy.Column(sqlalchemy.String, default='Не указан.')
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    balance = sqlalchemy.Column(sqlalchemy.Float, default=0)
    permission = sqlalchemy.Column(sqlalchemy.String)
    sum_rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    count_rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    last_changed_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    avatar_source = sqlalchemy.Column(sqlalchemy.String,
                                      default='default_avatar.png')
    products = orm.relation('Product', back_populates='user')
    if permission == 'seller':
        transactions = orm.relation('Transaction', back_populates='seller')
    elif permission == 'buyer':
        transactions = orm.relation('Transaction', back_populates='buyer')