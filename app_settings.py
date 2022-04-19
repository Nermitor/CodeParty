from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from config import BaseConfig
from data import db_session
from data.models.users import User

app = Flask(__name__)
app.config.update(BaseConfig.__dict__)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)
