from sqlalchemy import Column, String, Integer

from ..db_session import SqlAlchemyBase


class Language(SqlAlchemyBase):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    special_name = Column(String, index=True)
