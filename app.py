from time import sleep

from core.recommendations.index import index
from data import db_session
from app_settings import app, api
from threading import Thread


import views  # do not delete, connects views on import


def app_main():
    from apps import authorisation, profile, posts, follows
    api.add_resource(posts.models.resources.post.PostListResource, '/api/v2/posts')
    api.add_resource(posts.models.resources.post.PostResource, '/api/v2/posts/<int:post_id>')
    app.register_blueprint(authorisation.app.authorisation)
    app.register_blueprint(profile.app.profile)
    app.register_blueprint(posts.app.posts)
    app.register_blueprint(follows.app.follows)
    app.run()


def index_main():
    while True:
        sleep(10)
        index()


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    t2 = Thread(target=app_main)
    t1 = Thread(target=index_main)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
