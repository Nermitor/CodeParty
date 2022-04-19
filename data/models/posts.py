import datetime

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Integer, Boolean, Text, orm, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from ..db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    title = Column(String, nullable=True)
    code = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = orm.relation("User")

