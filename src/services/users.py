from sqlalchemy.orm import Session
from typing import Optional
from fastapi import status

from .base import BaseService
from src.dals import UserDAL
from src.models import User
from src.schemas import UserCreate, UserUpdate, UserInDB
from src.utils.security import get_password_hash, verify_password
from src.utils.service_result import ServiceResult
from src.utils.app_exceptions import AppException


class UserService(BaseService[UserDAL, UserCreate, UserUpdate]):
    def create(self, db: Session, obj_in: UserCreate):
        if self.dal(self.model).read_one_filtered_by_email(db, obj_in.email):
            return ServiceResult(AppException.BadRequest("This email is already taken"))
        db_obj = obj_in.dict(exclude={"password"})
        password = get_password_hash(obj_in.password)
        db_obj.update({"password": password, "is_active": False})
        return super().create(
            db, obj_in=UserInDB(**db_obj)
        )  # after modify had to unwrap as dal works with object-type BaseModel

    def get_one_by_email(self, db: Session, email):
        data = self.dal(self.model).read_one_filtered_by_email(db, email)
        if not data:
            return ServiceResult(
                AppException.NotFound(f"No user found with this email: {email}")
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_one_by_phone(self, db: Session, phone):
        data = self.dal(self.model).read_one_filtered_by_phone(db, phone)
        if not data:
            return ServiceResult(
                AppException.NotFound(f"No user found with this phone: {phone}")
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def update_by_id(self, db: Session, obj_in: UserUpdate):
        db_obj = obj_in.dict(exclude_unset=True)
        if obj_in["password"]:
            hashed_password = get_password_hash(obj_in.password)
            del obj_in["password"]
            obj_in["password"] = hashed_password
        return super().update_by_id(db, UserUpdate(**db_obj))

    def is_authenticated(
        self, db: Session, *, email: str, password: str  # * form kwargs
    ) -> Optional[User]:
        user = self.dal(self.model).read_one_filtered_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user_service = UserService(UserDAL, User)
