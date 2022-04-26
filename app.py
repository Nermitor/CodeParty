from app_settings import app
from core.recomendations.index import index
from apps import authorisation, profile, posts
from data import db_session
import views  # do not delete, connects views on import


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    index()
    app.register_blueprint(authorisation.app.authorisation)
    app.register_blueprint(profile.app.profile)
    app.register_blueprint(posts.app.posts)
    app.run()
