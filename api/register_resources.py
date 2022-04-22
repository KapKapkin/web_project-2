from flask_restful import Resource

from api.parser import registerparser
from data import db_session
from data.users import Users


class RegisterResource(Resource):
    def post(self):
        args = registerparser.parse_args()
        session = db_session.create_session()
        users = Users(
            name=args['name'],
            surname=args['surname'],
            email=args['email'],
            age=args['age'],
            tags=args['tags'],
        )
        users.set_password(args['password'])
        session.add(users)
        session.commit()