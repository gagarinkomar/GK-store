import os
import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    balance = sqlalchemy.Column(sqlalchemy.Float, default=0)
    permission = sqlalchemy.Column(sqlalchemy.String)
    sum_rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    count_rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    last_changed_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    avatar_source = sqlalchemy.Column(sqlalchemy.String,
                                      default=os.path.join(
                                          'static', 'img', 'default_avatar.png'
                                      ))
    products = orm.relation('Product', back_populates='user')
