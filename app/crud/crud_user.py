import datetime
from typing import Any, Dict, Optional, Union

from app.utils.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:  # noqa
        return db.query(User).where(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:  # noqa
        return db.query(User).where(User.username == username).first()

    def create(self, db: Session, obj_in: UserCreate, with_commit: bool = True) -> User:

        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name,
            last_name=obj_in.last_name,
            username=obj_in.username,
            created_at=datetime.datetime.now(),
            last_login_at=datetime.datetime.now()
        )
        # fixme: add user_x_role -_-
        if obj_in.username:
            db_obj.username = obj_in.username

        db.add(db_obj)
        if with_commit:
            db.commit()
            db.refresh(db_obj)

        return db_obj

    def update(
            self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserUpdate:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        user.last_login_at = datetime.datetime.now()
        return user

    def is_active(self, user: User) -> bool:  # noqa
        return user.is_active

    def is_superuser(self, user: User) -> bool:  # noqa
        return user.is_superuser

    def login_via_soc_nets(self, db: Session, username: str, access_token: str or None = None):
        user_in_db = db.query(User).where(User.username == username).first()
        data = {"last_login_at": str(datetime.datetime.now())}
        if access_token:
            data.update({"access_token": access_token})
        return self.update(db, db_obj=user_in_db, obj_in=data)


user = CRUDUser(User)
