from flask import redirect, render_template
from flask_login import current_user, login_required

from data import db_session
from data.models.users import User
from .app import follows


@follows.route('/id<user_id>/follows')
def follows_on_id(user_id):
    if user_id == current_user.id:
        return redirect('/follows/')
    with db_session.create_session() as db_sess:
        view_user = db_sess.query(User).get(user_id)
        return render_template(
            "follows/follows.html",
            users_list=view_user.follows.all(),
            title2=f"Подписки {view_user.nickname}"
        )


@follows.route('/follows/')
@follows.route('/profile/follows')
@login_required
def view_follows():
    with db_session.create_session() as db_sess:
        cur_user = db_sess.query(User).get(current_user.id)
        return render_template("follows/follows.html",
                               users_list=cur_user.follows.all(),
                               title2='Ваши Подписки')


@follows.route('/id<user_id>/followed')
def followed_on_id(user_id):
    if user_id == current_user.id:
        return redirect('/followed/')
    with db_session.create_session() as db_sess:
        view_user = db_sess.query(User).get(user_id)
        return render_template(
            "follows/follows.html",
            users_list=view_user.followers.all(),
            title2=f"Подписчики {view_user.nickname}"
        )


@follows.route('/followed')
@follows.route('/profile/followed')
@login_required
def followed():
    with db_session.create_session() as db_sess:
        cur_user = db_sess.query(User).get(current_user.id)
        return render_template("follows/follows.html",
                               users_list=cur_user.followers.all(),
                               title2='Ваши подписчики')


@follows.route("/id<user_id>/common_follows")
@login_required
def common_follows(user_id):
    with db_session.create_session() as db_sess:
        u1: User = db_sess.query(User).get(current_user.id)
        u2 = db_sess.query(User).get(user_id)
        return render_template("follows/follows.html",
                               users_list=u1.common_follows(u2).all(),
                               title2='Общие подписки')


@follows.route('/feed/')
@login_required
def feed():
    with db_session.create_session() as db_sess:
        cur_user: User = db_sess.query(User).get(current_user.id)
        return render_template("feed.html",
                               posts=cur_user.followed_posts())
