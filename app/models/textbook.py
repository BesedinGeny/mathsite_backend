from sqlalchemy import Column, Integer, String

from app.conf.db.base_tablename_class import Base


class Textbook(Base):
	__table_args__ = {
		"schema": "data",
	}
	id = Column(Integer, primary_key=True, autoincrement=True)
	school_class = Column(Integer, default=5)
	title = Column(String)
	slug = Column(String)
