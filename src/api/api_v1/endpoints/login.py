from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from src.api.deps import get_db
from src.schemas import Token
from src.services.users import user_service
from src.core.config import settings
from src.utils.security import create_access_token
from src.utils.service_result import ServiceResult
from src.utils.app_exceptions import AppException


router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_service.is_authenticated(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        return ServiceResult(AppException.BadRequest("Incorrect username or password"))
    elif user.is_active:
        return ServiceResult(AppException.BadRequest("User is inactive"))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
