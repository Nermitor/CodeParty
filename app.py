from app_settings import app
from apps import authorisation, profile
from data import db_session

if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.register_blueprint(authorisation.app.authorisation)
    app.register_blueprint(profile.app.profile)
    app.run()
