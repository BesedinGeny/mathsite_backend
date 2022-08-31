from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship

from app.conf.db.base_tablename_class import BaseWithId

USERS_SCHEMA = 'users'


class User(BaseWithId):
	"""
	Table with User Data
	"""
	__tablename__ = "user"
	__table_args__ = {"schema": USERS_SCHEMA,
	                  'comment': 'Table with all users'}
	
	name = Column(
		String, index=True,
		comment='name of user',
	)  # Имя
	middle_name = Column(
		String,
		comment='middle name of user',
	)  # Отчество
	last_name = Column(
		String, index=True,
		comment='last name of user',
	)  # Фамилия
	
	email = Column(
		String,
		unique=True,
		index=True,
		nullable=False,
		comment='email',
	)
	username = Column(
		String,
		unique=True,
		nullable=True,
		comment='username',
	)
	hashed_password = Column(
		String,
		nullable=False,
		comment='passwd',
	)
	
	is_active = Column(
		Boolean(),
		default=True,
		comment='locked or unlocked',
	)
	is_superuser = Column(
		Boolean(),
		default=False,
	)
	is_subscribed = Column(
		Boolean(),
		default=False,
	)
	
	created_at = Column(DateTime())
	updated_at = Column(DateTime())
	birth_date = Column(DateTime())
	subscription_ends = Column(DateTime())
	last_login_at = Column(DateTime())
	
	roles = relationship("UserXRole", back_populates="user", uselist=False)
