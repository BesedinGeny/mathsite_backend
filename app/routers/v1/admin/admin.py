from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from psycopg2.errors import UniqueViolation  # noqa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app import crud as crud
from app import models, schemas
from app.utils.security import check_for_permission, get_password_hash
from app.routers import deps
from app.schemas.role import RolesType

router = APIRouter()


@router.get("/users_list", response_model=LimitOffsetPage[schemas.User])
def get_users(
        db: Session = Depends(deps.get_db),
        permissions: list = Depends(deps.get_current_user_permission_list),
) -> Any:
    """
    Get list of all users. Available for SUPERUSER, ADMIN
    """
    check_for_permission('GET_USERS_LIST', permissions)
    users = paginate(db.query(models.User))
    return users


@router.get("/get_roles", response_model=schemas.RolesList)
def get_all_available_roles(
        db: Session = Depends(deps.get_db),
        permissions: list = Depends(deps.get_current_user_permission_list),
) -> Any:
    """
    Get list of all available roles in system. Available for SUPERUSER, ADMIN
    """
    check_for_permission('GET_ROLES', permissions)
    roles = crud.role.get_multi(db, skip=0, limit=100)
    all_roles = [r.name for r in roles]
    return {'roles': all_roles}


@router.post("/create_user", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        permissions: list = Depends(deps.get_current_user_permission_list),
) -> Any:
    """
    Create New user with access lower than current user access level
    """

    if user_in.role not in [RolesType.ADMIN, RolesType.CONTENT_MANAGER, RolesType.SEO_SPECIALIST]:
        raise HTTPException(detail='Incorrect role type. Please check it',
                            status_code=status.HTTP_400_BAD_REQUEST)
    required_permission = 'CREATE_ADMINS' if user_in.role == RolesType.ADMIN else \
        'CREATE_CONTENTS' if user_in.role == RolesType.CONTENT_MANAGER else \
        'CREATE_SEO' if user_in.role == RolesType.SEO_SPECIALIST else None

    if required_permission in permissions:
        user = crud.user.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        # Create the user
        user = crud.user.create(db, obj_in=user_in)

        # Add access
        role_id = crud.role.get_by_name(db, name=user_in.role).id

        role_in = schemas.UserXRoleCreate(
            user_id=user.id,
            role_id=role_id
        )
        crud.user_x_role.create(db, obj_in=role_in)  # noqa: F841
        db.commit()
        return user
    else:
        return JSONResponse({"msg": "Permission denied"},
                            status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(
        user_id: UUID,
        db: Session = Depends(deps.get_db),
        permissions: list = Depends(deps.get_current_user_permission_list),

) -> Any:
    """
    Get a specific user by id.
    """
    check_for_permission('GET_USER_LIST', permissions)
    return crud.user.get(db, obj_id=user_id)


@router.put("/{user_id}", response_model=schemas.User)
def update_user_profile(
        *,
        db: Session = Depends(deps.get_db),
        user_id: UUID,
        user_in: schemas.UserProfileUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
        permissions: list = Depends(deps.get_current_user_permission_list)
) -> Any:
    """
    Update a user profile.
    """
    user = crud.user.get(db, obj_id=user_id)

    if 'CHANGE_ANOTHER_USERS_PROFILE' in permissions and \
            current_user.roles.role.access_level < user.roles.role.access_level:

        if not user:
            raise HTTPException(
                detail="The user with this SID does not exist in the system",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            return crud.user.update(db, db_obj=user, obj_in=user_in)
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            raise HTTPException(detail='User with this email or phone',
                                status_code=status.HTTP_400_BAD_REQUEST)
    else:
        raise HTTPException(
            detail="Method not allowed!"
                   "Mb you try to change profile of user higher/same "
                   "access level or you have no this permission",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


@router.put("/password/{user_id}", response_model=schemas.Msg)
def change_another_user_password(
        *,
        db: Session = Depends(deps.get_db),
        user_id: UUID,
        new_password: str = Body(..., embed=True),
        current_user: models.User = Depends(deps.get_current_active_user),
        permissions: list = Depends(deps.get_current_user_permission_list)
) -> Any:
    """
    Update a password for another user with access_level lower than current user'.
    """
    user = crud.user.get(db, obj_id=user_id)

    if 'CHANGE_ANOTHER_USERS_PASSWORD' in permissions and \
            current_user.roles.role.access_level < user.roles.role.access_level:

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this SID does not exist in the system",
            )
        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password

        db.add(user)
        db.commit()

        return JSONResponse({"msg": "Password for user {} updated successfully".format(user_id)},
                            status_code=status.HTTP_200_OK)

    else:
        raise HTTPException(
            detail="Method not allowed!"
                   "Mb you try to change profile of user higher/same "
                   "access level or you have no this permission",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


@router.post("/lock/{user_id}", response_model=schemas.Msg)
def lock_unlock_users(
        *,
        db: Session = Depends(deps.get_db),
        user_id: UUID,
        current_user: models.User = Depends(deps.get_current_active_user),
        permissions: list = Depends(deps.get_current_user_permission_list)
) -> Any:
    """
    Block/Unlock user by SID.
    """
    user = crud.user.get(db, obj_id=user_id)
    if 'BLOCK_USERS' in permissions and \
            current_user.roles.role.access_level < user.roles.role.access_level:

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this SID does not exist in the system",
            )
        lock_status = user.is_active
        user.is_active = not lock_status

        db.add(user)
        db.commit()

        locked_message = 'blocked' if lock_status is True else 'unblocked'
        return {'msg': 'User {} {}'.format(user_id, locked_message)}

    else:
        raise HTTPException(
            detail="Method not allowed!"
                   "Mb you try to change profile of user higher/same "
                   "access level or you have no this permission",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
