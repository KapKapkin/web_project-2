from flask_restful import Resource, abort
from flask import Response, session
import json
from sqlalchemy import asc, or_
from sqlalchemy.sql.expression import func

from api.parser import messageparser
from data import db_session
from data.messages import Messages
from data.dialogs import Dialogs
from data.token import token_required


def abort_if_not_found(message_id):
    db_sess = db_session.create_session()
    messages = db_sess.query(Messages).get(message_id)
    if not messages:
        abort(404, message=f"Message {message_id} not found")


class MessagesResource(Resource):
    @token_required
    def get(user):
        args = messageparser.parse_args()
        print(args)
        db_sess = db_session.create_session()
        if args['user_id'] == 0:
            user_id = session['_recipient']
        else:
            user_id = args['user_id']
        if user.id == user_id:
            return Response(response=json.dumps({"Error": "same users ids"}), status=401)
        if args['count'] > 0:
            messages = db_sess.query(Messages).filter(Messages.sender_id.in_(
                [user.id, user_id]), Messages.recipient_id.in_([user.id, user_id])).order_by(Messages.id.desc()).limit(args['count']).all()
            messages.reverse()
        else:
            messages = db_sess.query(Messages).filter(Messages.sender_id.in_(
                [user.id, user_id]), Messages.recipient_id.in_([user.id, user_id]))  .all()
        return Response(response=json.dumps({'messages': [item.to_dict(
            only=('type', 'sender_id', 'recipient_id',
                  'dialog_id', 'send_time', 'content')
        ) for item in messages], 'user_id': user.id}), status=200)

    @token_required
    def post(user):
        args = messageparser.parse_args()
        db_sess = db_session.create_session()
        type = args['type']
        sender_id = user.id
        recipient_id = args['user_id']
        content = args['content']
        if recipient_id == 0:
            recipient_id = session['_recipient']
        dialog_id = db_sess.query(Dialogs).filter(Dialogs.user_one_id.in_(
            [sender_id, recipient_id]), Dialogs.user_two_id.in_([sender_id, recipient_id])).first()

        dialog_id = dialog_id.id

        if not dialog_id:
            return abort(
                404, message=f'Dialog {sender_id} - {recipient_id} not found')

        messages = Messages(
            type=type,
            sender_id=sender_id,
            recipient_id=recipient_id,
            dialog_id=dialog_id,
            content=content
        )
        db_sess.add(messages)
        db_sess.commit()
        return Response(response=json.dumps({'succes': 'OK'}), status=200)

    @token_required
    def delete(user):
        args = messageparser.parse_args()
        id = args['id']
        abort_if_not_found(id)
        db_sess = db_session.create_session()
        messages = db_sess.query(Messages).get(id)
        if messages.sender_id == user.id:
            return Response(response=json.dumps({'error': 'Messsage is not yours'}), status=401)
        db_sess.delete(messages)
        db_sess.commit()
        return Response(response=json.dumps({'succes': 'OK'}), status=200)
