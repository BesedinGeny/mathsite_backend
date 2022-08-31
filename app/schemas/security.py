from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from .permission import Permission


class PermissionXRoleBase(BaseModel):
    role_id: int
    permission_id: int

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class PermissionXRoleCreate(PermissionXRoleBase):
    updated_at: Optional[datetime]

    @validator("updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


# Properties to receive via API on update
class PermissionXRoleUpdate(PermissionXRoleBase):
    permission_id: Optional[int] = None
    role_id: Optional[int] = None
    updated_at: Optional[datetime]

    @validator("updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class PermissionXRoleInDBBase(PermissionXRoleBase):
    permission: Permission

    class Config:
        orm_mode = True


# Additional properties to return via API
class PermissionXRole(PermissionXRoleInDBBase):
    pass

    class Config:
        orm_mode = True


# Additional properties stored in DB
class PermissionXRoleInDB(PermissionXRoleInDBBase):
    pass


class UserXRoleBase(BaseModel):
    """
    Принадлежность пользователя конкретной роли
    """

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserXRoleCreate(UserXRoleBase):
    user_id: int
    role_id: int

    updated_at: Optional[datetime]

    @validator("updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


from .role import Role

# Properties to receive via API on update
class UserXRoleUpdate(UserXRoleBase):
    user_id: int
    role_id: int

    updated_at: Optional[datetime]

    @validator("updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class UserXRoleInDBBase(UserXRoleBase):
    pass


# Additional properties to return via API
class UserXRole(UserXRoleInDBBase):
    role: Role


# Additional properties stored in DB
class UserXRoleInDB(UserXRoleInDBBase):
    pass
