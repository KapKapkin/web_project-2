import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Dialogs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dialogs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_one_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    user_two_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)

    user_one = sqlalchemy.orm.relation('Users', foreign_keys=[user_one_id])
    user_two = sqlalchemy.orm.relation('Users', foreign_keys=[user_two_id])

    messages = sqlalchemy.orm.relation('Messages', back_populates='dialog',  cascade="all,delete")