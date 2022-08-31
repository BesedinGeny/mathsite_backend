from typing import List, Optional

from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str or None) -> Optional[str]:
	if password is None:
		return None
	return pwd_context.hash(password)


def check_for_permission(right: str, permissions: List[str]):
	if right not in permissions:
		raise HTTPException(detail="Method not allowed!",
		                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
