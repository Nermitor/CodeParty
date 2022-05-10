from flask import Flask, redirect
from flask_login import LoginManager, current_user
from flask_mail import Mail
from config import BaseConfig
import locale
from flask_restful import reqparse, abort, Api, Resource

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


app = Flask(__name__)
api = Api(app)

app.config.update(BaseConfig.__dict__)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)


