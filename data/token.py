import flask
import jwt

from flask_restful import wraps
from data import db_session
from data.users import Users


def token_required(f, *args, **kwargs):
    @wraps(f)
    def _verify(*args, **kwargs):
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }
        try:
            token = flask.request.json['token']
        except TypeError:
            try:
                if flask.session['logged_in'] == False:
                    raise Exception
                token = flask.session['_token']
            except (KeyError, Exception):
                return flask.jsonify(invalid_msg)
        try:
            session = db_session.create_session()
            data = jwt.decode(
                token, flask.current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = session.query(Users).filter(Users.email == data['email']).first()
            if not user:
                raise RuntimeError('User not found')
            flask.session['_user_id'] = user.id
            return f(user)
        except jwt.ExpiredSignatureError:
            return flask.jsonify(expired_msg)
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return flask.jsonify(invalid_msg)
    return _verify

def refresh_token():
    pass