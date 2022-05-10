import datetime

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Integer, Boolean, Text, orm, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .languages import Language
from ..db_session import SqlAlchemyBase


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    title = Column(String, nullable=True)
    code = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    comments = orm.relation("Comment", backref='post', lazy='dynamic')
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = orm.relation("Language", uselist=False)


