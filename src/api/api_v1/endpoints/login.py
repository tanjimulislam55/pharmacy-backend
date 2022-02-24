from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from db.config import get_db
from core.config import settings
from schemas import Token
from services import user_service
from utils.security import create_access_token
from utils.service_result import ServiceResult, handle_result
from utils.app_exceptions import AppException


router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_service.is_authenticated(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        return handle_result(
            ServiceResult(AppException.BadRequest("Incorrect username or password"))
        )
    elif not user.is_active:
        return handle_result(ServiceResult(AppException.BadRequest("User is inactive")))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
