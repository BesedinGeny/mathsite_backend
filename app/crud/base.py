from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from app.conf.db.base_tablename_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
	def __init__(self, model: Type[ModelType]):
		"""
		CRUD object with default methods to Create, Read, Update, Delete (CRUD).


		:param model: A SQLAlchemy model class
		:param schema: A Pydantic model (schema) class
		"""
		self.model = model
	
	def get(self, db: Session, obj_id: int) -> Optional[ModelType]:
		return db.query(self.model).filter(self.model.id == obj_id).first()
	
	def get_all(self, db: Session) -> Optional[ModelType]:
		return db.query(self.model).all()
	
	def get_multi(
			self, db: Session, skip: int = 0, limit: int = 100
	) -> List[ModelType]:
		return db.query(self.model).offset(skip).limit(limit).all()
	
	def create(
			self,
			db: Session,
			obj_in: CreateSchemaType,
			with_commit: bool = True
	) -> ModelType:
		obj_in_data = jsonable_encoder(obj_in)
		db_obj = self.model(**obj_in_data)  # type: ignore
		db.add(db_obj)
		if with_commit:
			db.commit()
			db.refresh(db_obj)
		return db_obj
	
	def update(
			self,
			db: Session,
			db_obj: ModelType,
			obj_in: Union[UpdateSchemaType, Dict[str, Any]]
	) -> ModelType:
		obj_data = jsonable_encoder(db_obj)
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		for field in obj_data:
			if field in update_data:
				setattr(db_obj, field, update_data[field])
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj
	
	def remove(self, db: Session, obj_id: int, soft_delete=False) -> ModelType:
		obj = db.query(self.model).filter(self.model.id == obj_id).first()
		if not obj:
			raise HTTPException(
				detail=f"Object with id '{obj_id}' was not found, nothing to delete",
				status_code=status.HTTP_400_BAD_REQUEST
			)
		if soft_delete:
			try:
				obj.is_active = False
			except Exception as e:
				""" Object has no attr 'is_active' """
				pass
		else:
			db.delete(obj)
		db.commit()
		return obj

