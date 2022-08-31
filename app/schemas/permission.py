from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class PermissionBase(BaseModel):
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class PermissionCreate(PermissionBase):
    name: str
    description: str

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


# Properties to receive via API on update
class PermissionUpdate(PermissionBase):
    name: str
    description: str

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class PermissionInDBBase(PermissionBase):
    name: str
    description: str

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


# Additional properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass
