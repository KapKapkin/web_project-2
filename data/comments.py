import sqlalchemy 
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id'), nullable=False)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    post = sqlalchemy.orm.relation('Posts', foreign_keys=[post_id])
    user = sqlalchemy.orm.relation('Users', foreign_keys=[owner_id])
