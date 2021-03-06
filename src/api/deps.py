from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import jwt

from schemas import TokenPayload
from models import User
from services.users import user_service
from core.config import settings
from db.config import get_db
from utils.service_result import ServiceResult, handle_result
from utils.app_exceptions import AppException


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        return ServiceResult(AppException.CredentialsException())

    return user_service.get_one_by_email(db, email=token_data.sub)


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    # equivalent code: getattr(handle_result(current_user), "is_active", bool)
    if not handle_result(current_user).is_active:
        return ServiceResult(AppException.Forbidden("Inactive user"))

    return current_user


# def get_current_active_superuser(
#     current_user: User = Depends(get_current_user),
# ) -> User:
#     if not current_user.is_superuser:
#         return ServiceResult(
#             AppException.Forbidden("The user doesn't have enough privileges")
#         )
#     return current_user
