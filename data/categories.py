import sqlalchemy

from .db_session import SqlAlchemyBase


product_to_category_table = sqlalchemy.Table('product_to_category',
                                     SqlAlchemyBase.metadata,
    sqlalchemy.Column('product', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('categories.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)