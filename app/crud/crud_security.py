import datetime
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.security import Permission, Role, PermissionXRole, UserXRole
from app.schemas import (PermissionCreate, PermissionUpdate,
                         RoleCreate, RoleUpdate,
                         PermissionXRoleCreate, PermissionXRoleUpdate,
                         UserXRoleCreate, UserXRoleUpdate)


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    @staticmethod
    def get_by_name(db: Session, *, name: str) -> Permission:
        return db.query(Permission).filter(Permission.name == name).first()

    def get_all(self, db: Session) -> List[Permission]:
        return db.query(Permission).all()


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    @staticmethod
    def get_by_name(db: Session, *, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()

    def get_all(self, db: Session) -> List[Role]:
        return db.query(Role).all()


class CRUDPermissionXRole(CRUDBase[PermissionXRole, PermissionXRoleCreate, PermissionXRoleUpdate]):
    @staticmethod
    def get_by_permission_and_role(db: Session, *,
                                   permission_id: UUID, role_id: UUID) -> PermissionXRole:
        return db.query(PermissionXRole).filter(PermissionXRole.permission_id == permission_id,
                                                PermissionXRole.role_id == role_id).first()


class CRUDUserXRole(CRUDBase[UserXRole, UserXRoleCreate, UserXRoleUpdate]):

    def create(self, db: Session, *, obj_in: UserXRoleCreate, with_commit: bool = True) -> UserXRole:
        db_obj = UserXRole(
            user_id=obj_in.user_id,
            role_id=obj_in.role_id,
            updated_at=datetime.datetime.now()
        )
        db.add(db_obj)
        if with_commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj


role = CRUDRole(Role)
permission = CRUDPermission(Permission)
permission_x_role = CRUDPermissionXRole(PermissionXRole)
user_x_role = CRUDUserXRole(UserXRole)
