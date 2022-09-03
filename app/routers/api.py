from fastapi import APIRouter

from app.routers.v1.auth import auth
from app.routers.v1.users import users
from app.routers.v1.class_base_view import router2

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(router2, tags=["Test2"])
