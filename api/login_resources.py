from flask_restful import Resource
from flask import jsonify, Response, current_app
import json
import jwt
from datetime import datetime, timedelta


from api.parser import loginparser
from data import db_session
from data.users import Users


class LoginResource(Resource):
    def post(self):
        args = loginparser.parse_args()
        session = db_session.create_session()
        user = session.query(Users).filter(Users.email == args['email']).first()
        if not user:
            return Response(response=json.dumps({'message': 'Invalid credentials', 'authenticated': False}), status=401)
        if not user.check_password(args['password']):
            return Response(response=json.dumps({'message': 'Invalid password or email', 'authenticated': False}), status=401)
  
        token = jwt.encode({
            'user': user.id,
            'email': user.email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24)},
            current_app.config['SECRET_KEY'])
        
        return Response(response=json.dumps({"token": token}), status=200)
