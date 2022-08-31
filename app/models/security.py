import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.conf.db.base_tablename_class import Base, BaseWithId

if TYPE_CHECKING:
    from .user import User  # noqa: F401

SECURITY_SCHEMA = 'security'


class Role(BaseWithId):
    __tablename__ = "role"
    __table_args__ = {"schema": SECURITY_SCHEMA}

    name = Column(String, unique=True,
                  index=True, nullable=False)
    description = Column(String, nullable=False)
    access_level = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)

    users = relationship("UserXRole", back_populates="role")
    permissions = relationship('PermissionXRole', back_populates="role")


class Permission(BaseWithId):
    __tablename__ = "permission"
    __table_args__ = {"schema": SECURITY_SCHEMA}

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)

    roles = relationship("PermissionXRole", back_populates="permission")


class UserXRole(Base):
    __tablename__ = "user_x_role"
    __table_args__ = {"schema": SECURITY_SCHEMA}
    
    user_id = Column(
        Integer,
        ForeignKey("users.user.id"),
        nullable=False, primary_key=True
    )
    role_id = Column(
        Integer,
        ForeignKey("security.role.id"),
        nullable=False, primary_key=True
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.datetime.now
    )

    role = relationship("Role", back_populates="users")
    user = relationship("User", back_populates="roles")

    def __init__(self, user_id, role_id, updated_at=None):
        self.user_id = user_id
        self.role_id = role_id
        self.updated_at = updated_at


class PermissionXRole(Base):
    __tablename__ = "permission_x_role"
    __table_args__ = {"schema": SECURITY_SCHEMA}

    permission_id = Column(
        Integer,
        ForeignKey("security.permission.id"),
        primary_key=True
    )
    role_id = Column(
        Integer,
        ForeignKey("security.role.id"),
        primary_key=True
    )

    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")

    def __init__(self, permission_id, role_id, updated_at=None):
        self.permission_id = permission_id
        self.role_id = role_id
        self.updated_at = updated_at

