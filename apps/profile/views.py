from flask import render_template, redirect, make_response
from flask_login import current_user, login_required, logout_user

from data import db_session
from data.models.users import User
from .app import profile


@profile.route("/id<uid>/")
def profile_on_id(uid):
    if current_user.is_authenticated:
        if current_user.id == uid:
            return redirect('/profile')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(uid)
    if user:
        return render_template("profile/profile.html", user=user)


@profile.route("/profile/")
@login_required
def profile_route1():
    return render_template("profile/profile.html", user=current_user)


@profile.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect('/')


@profile.route('/id<user_id>/avatar/')
def avatar(user_id):
    db_sess = db_session.create_session()
    user_avatar = db_sess.query(User).get(user_id).get_avatar()
    h = make_response(user_avatar)
    h.headers['Content-Type'] = 'image/png'
    return h