from flask import redirect
from flask_login import current_user, login_manager

from app_settings import app, login_manager
from data import db_session
from data.__all_models import User


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/profile')
    return redirect("/login")
