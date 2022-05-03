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
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).get(uid)
        if user:
            print(user.posts)
            return render_template("profile/profile.html",
                                   user=user,
                                   current_user=db_sess.query(User).get(current_user.id))


@profile.route("/profile/")
@login_required
def profile_route1():
    with db_session.create_session() as db:
        return render_template("profile/profile.html",
                               user=db.query(User).get(current_user.id))


@profile.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect('/')


@profile.route('/id<user_id>/avatar/')
def avatar(user_id):
    with db_session.create_session() as db_sess:
        user_avatar = db_sess.query(User).get(user_id).get_avatar()
    h = make_response(user_avatar)
    h.headers['Content-Type'] = 'image/png'
    return h


@profile.route("/id<user_id>/subscribe/")
@login_required
def subscribe(user_id):
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).get(user_id)
        current_user_on_sess: User = db_sess.query(User).get(current_user.id)
        if current_user_on_sess.is_following(user):
            current_user_on_sess.unfollow(user)
        else:
            current_user_on_sess.follow(user)
        db_sess.commit()
    return redirect(f'/id{user_id}')

