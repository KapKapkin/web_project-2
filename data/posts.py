import sqlalchemy 
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Posts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    #image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    user = sqlalchemy.orm.relation('Users', foreign_keys=[owner])

    comments = sqlalchemy.orm.relation('Comments', back_populates='post', cascade='all,delete')