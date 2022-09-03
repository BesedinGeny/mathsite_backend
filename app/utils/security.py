from typing import List, Optional, Tuple

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


def check_for_permission(required_rights: str | Tuple, permissions: List[str]):
	"""throw error if even one right not included in required permissions """
	if isinstance(required_rights, str):
		required_rights = (required_rights,)

	for right in required_rights:
		if right not in permissions:
			raise HTTPException(detail="Method not allowed!",
								status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
