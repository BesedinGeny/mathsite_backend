from typing import Type, Tuple, Generic, TypeVar

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.conf.db.base_tablename_class import Base

# router = InferringRouter()
from app.crud.base import CRUDBase
from app.routers.deps import *
#
# ModelType = TypeVar("ModelType", bound=Base)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)


def CRUDEndpointFactory(
        Model: Type[Base],
        CreateSchema: Type[BaseModel],
        UpdateSchema: Type[BaseModel],
        ResponseSchema: Type[BaseModel],
        crud_obj: CRUDBase,
        router: InferringRouter = InferringRouter()
):
    ModelType = TypeVar("ModelType", bound=Model)
    CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchema)
    UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchema)
    ResponseSchemaType = TypeVar("ResponseSchemaType", bound=ResponseSchema)
    prefix = "/" + Model.__tablename__

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
        ) -> ResponseSchemaType:
            model_obj = self.__crud_obj.get(db, obj_id=obj_id)
            return ResponseSchema.from_orm(model_obj)

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

