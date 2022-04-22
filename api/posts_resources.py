from flask_restful import Resource, abort
from flask import jsonify

from api.parser import postsparser
from data import db_session
from data.posts import Posts
from data.token import token_required


def abort_if_post_not_found(posts_id):
    session = db_session.create_session()
    users = session.query(Posts).get(posts_id)
    if not users:
        abort(404, message=f"Users {posts_id} not found")


class PostsListResource(Resource):
    @token_required
    def get(user):
        args = postsparser.parse_args()
        db_sess = db_session.create_session()
        posts = db_sess.query(Posts).filter(Posts.owner.like(args['owner'])).all()
        return jsonify({'posts': [post.to_dict(only=['id', 'content', 'owner', 'time']) for post in posts]})

    @token_required
    def post(user):
        db_sess = db_session.create_session()
        args = postsparser.parse_args()
        content = args['content']
        time = args['time']

        post = Posts(content=content, owner=user.id, time=time)   
        db_sess.add(post)
        db_sess.commit()
        return jsonify({'succes': 'OK'})
    
    @token_required
    def delete(user):
        args = postsparser.parse_args()
        posts_id = args['posts_id']

        abort_if_post_not_found(posts_id)
        db_sess = db_session.create_session()
        posts = db_sess.query(Posts).get(posts_id)
        if posts.owner != user.id:
            return jsonify({'Error': 'This post is not yours'})

        db_sess.delete(posts)
        db_sess.commit()
        return jsonify({'Succes': 'OK'})
 