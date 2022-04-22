from flask_restful import Resource, abort
from flask import Response
import json

from sqlalchemy import or_

from data.token import token_required

from api.parser import dialogparser
from data import db_session
from data.dialogs import Dialogs


def abort_if_dialogs_not_found(user_one_id, user_two_id):
    db_sess = db_session.create_session()
    dialogs = db_sess.query(Dialogs).filter(Dialogs.user_one_id.in_(
        [user_one_id, user_two_id]), Dialogs.user_two_id.in_([user_one_id, user_two_id])).first()

    if not dialogs or user_one_id == user_two_id:
        abort(404, message=f"Dialogs {user_one_id} - {user_two_id} not found")
    return dialogs.id




class DialogsListResource(Resource):
    @token_required
    def get(user):
        
        args = dialogparser.parse_args()
        user_id = args['user_id']

        db_sess = db_session.create_session()
        if user_id !='%%':
            dialogs = db_sess.query(Dialogs).filter(Dialogs.user_one_id.in_([user.id, user_id]), Dialogs.user_two_id.in_([user.id, user_id])).all()
        else:
            dialogs = db_sess.query(Dialogs).filter(or_(Dialogs.user_one_id == user.id, Dialogs.user_two_id == user.id)).all()
            
        return Response(response=json.dumps({'dialogs': [item.to_dict(
           only=('user_one_id', 'user_two_id', "id")
        ) for item in dialogs], 'user_id':user.id}), status=200)

    @token_required
    def post(user):
        args = dialogparser.parse_args()

        
        user_id = args['user_id']
        db_sess = db_session.create_session()
        dialogs = db_sess.query(Dialogs).filter(Dialogs.user_one_id.in_(
            [user.id, user_id]), Dialogs.user_two.in_([user.id, user_id])).first()

        if dialogs or user_id == user.id:
            abort(404, message=f"Error")

        dialogs = Dialogs(
            user_one_id=user.id,
            user_two_id=user_id
        )
        db_sess.add(dialogs)
        db_sess.commit()
        return Response(response=json.dumps({"succes":"OK"}), status=200)

    @token_required
    def delete(user):
        args = dialogparser.parse_args()

        user_id = args['user_id']

        dialogs_id = abort_if_dialogs_not_found(user.id, user_id)

        db_sess = db_session.create_session()
        dialogs = db_sess.query(Dialogs).get(dialogs_id)

        db_sess.delete(dialogs)
        db_sess.commit()
        return Response(response=json.dumps({"succes":"OK"}), status=200)
