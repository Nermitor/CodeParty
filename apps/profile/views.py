from flask import render_template, redirect
from flask_login import current_user

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