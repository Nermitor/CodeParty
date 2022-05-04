from flask import render_template, redirect
from flask_login import login_required, current_user

from data import db_session
from data.models.languages import Language
from data.models.posts import Post
from data.models.users import User
from .app import posts
from .models.forms.post import PostForm


@posts.route('/id<user_id>/posts/')
def user_all_posts(user_id):
    with db_session.create_session() as db_sess:
        user: User = db_sess.query(User).get(user_id)
        all_posts = user.posts
        return render_template("posts/all_posts.html", user=user, posts=all_posts)


@posts.route('/profile/new_post/', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            post = Post(
                user_id=current_user.id,
                title=form.title.data,
                code=form.code.data,
                language=db_sess.query(Language).get(form.language.data)
            )
            db_sess.add(post)
            db_sess.commit()
        return redirect("/profile/")
    return render_template("posts/new_post.html", form=form)


@posts.route('/post<post_id>')
def post(post_id):
    with db_session.create_session() as db_sess:
        cur_post = db_sess.query(Post).get(post_id)
        return render_template("posts/post.html", post=cur_post)
