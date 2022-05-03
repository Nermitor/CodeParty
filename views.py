from flask import redirect, render_template
from flask_login import current_user, login_manager, login_required

from app_settings import app, login_manager
from data import db_session
from data.__all_models import User


@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as db_sess:
        return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/profile')
    return redirect("/login")


@app.route('/recommendations')
@login_required
def view_recommendations():
    with db_session.create_session() as db_sess:
        cur_user = db_sess.query(User).get(current_user.id)
        return render_template("recommendations/recommendations.html",
                               users_list=cur_user.recommendations.all())


