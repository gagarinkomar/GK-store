import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Transaction(SqlAlchemyBase):
    __tablename__ = 'transactions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    buyer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    product_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('products.id'))
    status = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    price = sqlalchemy.Column(sqlalchemy.Float)
    estimate_seller = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    estimate_buyer = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    seller = orm.relationship('User', foreign_keys='Transaction.seller_id')
    buyer = orm.relationship('User', foreign_keys='Transaction.buyer_id')
    product = orm.relation('Product')
