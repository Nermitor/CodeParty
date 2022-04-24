from app_settings import app
from apps import authorisation, profile
from data import db_session
import views


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.register_blueprint(authorisation.app.authorisation)
    app.register_blueprint(profile.app.profile)
    app.run()
    # sess = db_session.create_session()
    # user = sess.query(User).get(1)
    # user2 = sess.query(User).get(2)
    # user.follow(user2)
    # print(user.follows.all())
