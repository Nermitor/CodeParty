import datetime
from sqlalchemy import Column, DateTime, String, Integer, Boolean, Text, orm, ForeignKey
from ..db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = "comments"
    id = Column(Integer, autoincrement=True, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String, nullable=False)