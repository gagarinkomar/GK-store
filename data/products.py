import os
import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    title = sqlalchemy.Column(sqlalchemy.String)
    short_about = sqlalchemy.Column(sqlalchemy.String)
    about = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Float)
    purchased_content = sqlalchemy.Column(sqlalchemy.String)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_sold = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_checked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    checked_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     nullable=True)
    image_source = sqlalchemy.Column(sqlalchemy.String,
                                     default='default_image.png')
    last_changed_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user = orm.relation('User')
    categories = orm.relation('Category',
                              secondary='product_to_category',
                              backref='products')
    transactions = orm.relation('Transaction', back_populates='product')
