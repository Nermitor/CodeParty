import datetime

from flask_login import UserMixin
from sqlalchemy import Column, DateTime, String, Integer, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from ..db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    confirmed = Column(Boolean, default=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
