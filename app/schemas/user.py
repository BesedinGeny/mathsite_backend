import string
from typing import Optional

from pydantic import EmailStr

from .core import CoreModel
from .security import UserXRole


class UserBase(CoreModel):
    name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str]
    username: Optional[str]


class SideUserCreate(UserBase):
    email: Optional[EmailStr]
    password: Optional[str]
    username: Optional[str]


# Properties to receive via API on update

class UserUpdate(UserBase):
    password: str


class UserProfileUpdate(UserBase):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    roles: Optional[UserXRole]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class Tokens(CoreModel):
    service: str
    access_token: str
    refresh_token: Optional[str]
