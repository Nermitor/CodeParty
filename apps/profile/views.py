from flask import render_template, redirect, make_response
from flask_login import current_user, login_required, logout_user

from data import db_session
from data.models.users import User
from .app import profile


@profile.route("/profile/id<uid>")
def profile_on_id(uid):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(uid)
    if user:
        print(user.languages)
        return render_template("profile/profile.html", user=user)


@profile.route("/profile/")
def profile_route1():
    return redirect('/profile/id{0}'.format(current_user.id))


@profile.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@profile.route('/profile/avatar/<user_id>')
def avatar(user_id):
    db_sess = db_session.create_session()
    user_avatar = db_sess.query(User).get(user_id).get_avatar()
    h = make_response(user_avatar)
    h.headers['Content-Type'] = 'image/png'
    return h