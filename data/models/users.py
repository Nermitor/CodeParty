import datetime
import sqlalchemy
from flask import url_for, make_response
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Integer, Boolean, orm, Text, ForeignKey, BLOB
from werkzeug.security import generate_password_hash, check_password_hash

from app_settings import app
from .posts import Post
from .. import db_session
from ..db_session import SqlAlchemyBase

followers = sqlalchemy.Table(
    'followers',
    SqlAlchemyBase.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)

recommendations = sqlalchemy.Table(
    'recommendations',
    SqlAlchemyBase.metadata,
    Column('recommended_for', Integer, ForeignKey('users.id')),
    Column('who_recommended', Integer, ForeignKey('users.id'))
)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    confirmed = Column(Boolean, default=False)

    about = Column(Text, nullable=True)
    languages = Column(String, nullable=True)
    avatar = Column(BLOB, nullable=True)

    posts = orm.relation("Post", backref='author', lazy='dynamic')
    comments = orm.relation("Comment", backref='author', lazy='dynamic')

    followed = orm.relation(
        "User", secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=orm.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    recommendations = orm.relation(
        "User", secondary=recommendations,
        primaryjoin=(recommendations.c.recommended_for == id),
        secondaryjoin=(recommendations.c.who_recommended == id),
        backref=orm.backref("recommended_for", lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f"(User №{self.id} | name = '{self.nickname}' | email = {self.email} |)"

    def __str__(self):
        return f"(User №{self.id} | name = '{self.nickname}' | email = {self.email} |)"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    @property
    def followers(self):
        return self.followed.filter(followers.c.followed_id == self.id)

    @property
    def follows(self):
        return self.followed.filter(followers.c.follower_id == self.id)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def common_follows(self, user):
        return self.follows.intersect(user.follows)

    def get_avatar(self):
        if not self.avatar:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='img/default.png'), 'rb') as f:
                    return f.read()
            except FileNotFoundError:
                print("Файла нет")
            except Exception as e:
                print(e)
        return self.avatar

    def set_avatar(self, avatar):
        with db_session.create_session() as db_sess:
            self.avatar = avatar
            db_sess.commit()

    def followed_posts(self):
        with db_session.create_session() as db_sess:
            return db_sess.query(Post).join(followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(Post.created_date.desc()).limit(50)

    @staticmethod
    def verify_ext(filename):
        ext = filename.rsplit('.', 1)[1]
        if ext.lower() in app.config['AVATAR_FILE_EXTENSIONS']:
            return True
        return False







