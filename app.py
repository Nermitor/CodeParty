from flask import Flask
from flask_mail import Mail
from config import BaseConfig

from apps.authorization import app as auth_app
from data import db_session

app = Flask(__name__)
app.config.update(BaseConfig.__dict__)

mail = Mail(app)

if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.register_blueprint(auth_app.authorisation)
    app.run()
