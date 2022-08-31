import json
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud as crud
from app import models
from app.conf.db.session import SessionLocal
from app.conf.settings import settings


@AuthJWT.load_config
def get_config():
    return settings


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends(),
) -> models.User:
    Authorize.jwt_required()

    payload_json = Authorize.get_jwt_subject()
    payload = json.loads(payload_json)

    user_in_db = crud.user.get(db, obj_id=payload['id'])

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # permissions = payload.get('permissions', [])  # Will be used in future
    return user_in_db


async def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inactive user")
    return current_user


async def get_current_user_permission_list(
        current_user: models.User = Depends(get_current_user)) -> list:
    user_permissions = current_user.roles.role.permissions
    return [p.permission.name for p in user_permissions]
