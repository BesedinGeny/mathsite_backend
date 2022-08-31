from sqlalchemy import Column, Integer, String

from app.conf.db.base_tablename_class import BaseWithId


class Textbook(BaseWithId):
	school_class = Column(Integer, default=5)
	title = Column(String)
	slug = Column(String)
