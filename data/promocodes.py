import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Promocode(SqlAlchemyBase):
    def set_content(self, content):
        self.hashed_content = generate_password_hash(content)

    def check_content(self, content):
        return check_password_hash(self.hashed_content, content)


    __tablename__ = 'promocodes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    hashed_content = sqlalchemy.Column(sqlalchemy.String)
    award = sqlalchemy.Column(sqlalchemy.Float)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_activated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)