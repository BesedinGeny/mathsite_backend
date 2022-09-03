from fastapi import APIRouter

from app.routers.v1.auth import auth
from app.routers.v1.users import users

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(users.router, tags=["Users"])

