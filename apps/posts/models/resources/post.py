from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.__all_models import Post

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('code', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('language_id', required=True, type=int)


def abort_if_post_not_found(post_id):
    session = db_session.create_session()
    news = session.query(Post).get(post_id)
    if not news:
        abort(404, message=f"Post {post_id} not found")


class PostResource(Resource):
    def get(self, post_id):
        abort_if_post_not_found(post_id)
        with db_session.create_session() as session:
            post = session.query(Post).get(post_id)
            return jsonify(
                {
                    'post': post.to_dict(only=(
                        "title", "created_date", "code", "user_id",
                    ))
                }
            )

    def delete(self, post_id):
        abort_if_post_not_found(post_id)
        with db_session.create_session() as session:
            post = session.query(Post).get(post_id)
            session.delete(post)
            session.commit()
        return jsonify({"success": "OK"})


class PostListResource(Resource):
    def get(self):
        with db_session.create_session() as session:
            posts = session.query(Post).all()
            return jsonify({'posts':
                            [item.to_dict(
                                only=('title', 'created_date', 'code', 'user_id')
                            ) for item in posts]})

    def post(self):
        args = parser.parse_args()
        with db_session.create_session() as session:
            post = Post(
                title=args['title'],
                code=args['code'],
                language_id=args['language_id'],
                user_id=args['user_id']
            )
            session.add(post)
            session.commit()
            return jsonify({"success": "OK"})
