from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, validator

from .security import PermissionXRole


class RolesType(str, Enum):
    ADMIN = "SUPERUSER"
    CONTENT_MANAGER = "TEACHER"
    SEO_SPECIALIST = "USER"


class RoleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    name: str
    description: str
    access_level: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    name: str
    description: str
    access_level: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class RoleInDBBase(RoleBase):
    name: str
    description: str
    access_level: int

    permissions: Optional[List[PermissionXRole]]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Role(RoleInDBBase):
    pass


# Additional properties stored in DB
class RoleInDB(RoleInDBBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class RolesList(BaseModel):
    roles: list
