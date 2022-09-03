import json
from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud as crud
from app import models
from app.conf.db.session import SessionLocal
from app.conf.settings import settings


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user_or_none(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
) -> Optional[models.User]:
    try:
        Authorize.jwt_required()
    except:
        return None
    payload_json = Authorize.get_jwt_subject()
    payload = json.loads(payload_json)

    user_in_db = crud.user.get(db, obj_id=payload['id'])
    return user_in_db


async def get_current_user(
        user_in_db: models.User = Depends(get_current_user_or_none)
) -> models.User:

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_in_db


async def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inactive user")
    return current_user


async def get_current_user_permission_list(
        current_user: models.User = Depends(get_current_user_or_none)
) -> list:
    if not current_user:
        return []
    user_permissions = current_user.roles.role.permissions
    return [p.permission.name for p in user_permissions]
