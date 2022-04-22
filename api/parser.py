from flask_restful import reqparse
from datetime import datetime
from flask import session

userparser = reqparse.RequestParser()
userparser.add_argument('user_id', required=False)
userparser.add_argument('name', required=False, )
userparser.add_argument('surname', required=False)
userparser.add_argument('age', required=False, type=int)
userparser.add_argument('email', required=False)
userparser.add_argument('tags', required=False, default=None)
userparser.add_argument('count', required=False, default=10, type=int)
userparser.add_argument('password', required=False, type=int)

dialogparser = reqparse.RequestParser()
dialogparser.add_argument('user_id', required=False, type=int, default='%%')
dialogparser.add_argument('count', required=False, default=10, type=int)

messageparser = reqparse.RequestParser()
messageparser.add_argument('type', required=False, default='text', type=str)
messageparser.add_argument('user_id', required=False, type=int, default=0)
messageparser.add_argument('content', required=False)
messageparser.add_argument('count', required=False, default=10, type=int)

registerparser = reqparse.RequestParser()
registerparser.add_argument('name', required=True)
registerparser.add_argument('surname', required=True)
registerparser.add_argument('age', required=True, type=int)
registerparser.add_argument('email', required=True)
registerparser.add_argument('tags', required=False, default=None)
registerparser.add_argument('password', required=True)

loginparser = reqparse.RequestParser()
loginparser.add_argument('email', required=True)
loginparser.add_argument('password', required=True)

postsparser = reqparse.RequestParser()
postsparser.add_argument('posts_id', required=False, type=int)
postsparser.add_argument('content', required=False, default='%%')
postsparser.add_argument('image', required=False, default='%%')
postsparser.add_argument('owner', required=False, default='%%')
postsparser.add_argument('time', required=False, default=datetime.now)
