from typing import Type, Tuple, Generic, TypeVar

from fastapi import Depends
from fastapi_pagination import LimitOffsetPage, paginate
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.conf.db.base_tablename_class import Base

# router = InferringRouter()
from app.crud.base import CRUDBase
from app.routers.deps import *
from app.utils.security import check_for_permission

# note: dict is mutable type, DANGER
"""
dont need permission to get objects, but need specific permission
"""
default_permission_map = {
    'single': (),
    'list': (),
    'create': ('CREATE_OBJECT', ),
    'update': ('EDIT_OBJECT', ),
    'delete': ('BLOCK_OBJECT', ),
}


def CRUDEndpointFactory(
        Model: Type[Base],
        CreateSchema: Type[BaseModel],
        UpdateSchema: Type[BaseModel],
        ResponseSchema: Type[BaseModel],
        crud_obj: CRUDBase,
        permission_map: dict = default_permission_map  # noqa
):
    """
    :param Model: SQLAlchemy model class
    :param CreateSchema: Pydantic create schema class
    :param UpdateSchema: Pydantic update schema class
    :param ResponseSchema: Pydantic response schema which will be returned from api
    :param crud_obj: CRUD-object which implement crud logic
    :param permission_map: Dict with keys 'single', 'list', 'create', 'update', 'delete' and values
     like tuple of strs of permissions for each
    """
    router = InferringRouter()
    ModelType = TypeVar("ModelType", bound=Model)
    CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchema)
    UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchema)
    ResponseSchemaType = TypeVar("ResponseSchemaType", bound=ResponseSchema)
    prefix = '/' + Model.__tablename__ + 's'

    @cbv(router)
    class BaseView(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
        """Предоставляет интерфейс для создания crud-endpoint-ов для наследствующих объекитов"""
        __prefix = prefix
        __crud_obj = crud_obj

        @router.get(__prefix)
        def get_single(
                self,
                obj_id: int,
                db: Session = Depends(get_db),
                permissions: list = Depends(get_current_user_permission_list)
        ) -> ResponseSchemaType:
            """Get single object by id"""
            check_for_permission(permission_map['single'], permissions)
            model_obj = self.__crud_obj.get(db, obj_id=obj_id)
            return ResponseSchema.from_orm(model_obj)

        @router.get(__prefix + '_list')
        def get_many(
                self,
                db: Session = Depends(get_db),
                permissions: list = Depends(get_current_user_permission_list)
        ) -> LimitOffsetPage[ResponseSchemaType]:
            """Get Paginated list of objects"""
            # note: можно ускорить работу путем написания собственной пагниации и get_multy
            check_for_permission(permission_map['list'], permissions)
            model_objs = self.__crud_obj.get_all(db)
            return paginate(model_objs)  # noqa

        @router.post(__prefix)
        def create(
                self,
                obj_in: CreateSchemaType,
                db: Session = Depends(get_db),
                permissions: list = Depends(get_current_user_permission_list)
        ) -> ResponseSchemaType:
            """ Create an object if user has enough rights """
            check_for_permission(permission_map['create'], permissions)
            created_obj = self.__crud_obj.create(db, obj_in)
            return ResponseSchema.from_orm(created_obj)

        @router.put(__prefix)
        def update(
                self,
                obj_id: int,
                obj_in: UpdateSchemaType,
                db: Session = Depends(get_db),
                permissions: list = Depends(get_current_user_permission_list)
        ) -> ResponseSchemaType:
            """ Update object with id=obj_id with data=obj_in if user has enough rights """
            check_for_permission(permission_map['update'], permissions)
            model_obj = self.__crud_obj.get(db, obj_id)
            if not model_obj:
                raise HTTPException(
                    detail=f"Object with id '{obj_id}' was not found, changes aborted",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            created_obj = self.__crud_obj.update(db, model_obj, obj_in)
            return ResponseSchema.from_orm(created_obj)

        @router.delete(__prefix)
        def delete(
                self,
                obj_id: int,
                db: Session = Depends(get_db),
                permissions: list = Depends(get_current_user_permission_list)
        ) -> ResponseSchemaType:
            """ Delete object with id=obj_id from database if user has enough rights"""
            check_for_permission(permission_map['delete'], permissions)
            removed_obj = self.__crud_obj.remove(db, obj_id)
            return removed_obj

    return router

# example

from app.models import User
from app.schemas import User as UserResponse, UserCreate, UserProfileUpdate
from app.crud import user

router2 = CRUDEndpointFactory(
    User,
    UserCreate,
    UserProfileUpdate,
    UserResponse,
    user
)

