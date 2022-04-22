import sqlalchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Messages(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, default='text')
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    recipient_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    dialog_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('dialogs.id'), nullable=False)
    send_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    sender = sqlalchemy.orm.relation('Users', foreign_keys=[sender_id])
    recipient = sqlalchemy.orm.relation('Users', foreign_keys=[recipient_id])

    dialog = sqlalchemy.orm.relation('Dialogs', foreign_keys=[dialog_id])
    
    
    