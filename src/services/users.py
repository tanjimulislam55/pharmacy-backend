from sqlalchemy.orm import Session
from typing import Optional
from fastapi import status

from .base import BaseService
from dals import UserDAL
from models import User
from schemas import UserCreate, UserUpdate, UserInDB, PharmacyCreate
from .pharmacies import pharmacy_service
from .roles import role_service
from utils.security import get_password_hash, verify_password
from utils.service_result import ServiceResult, handle_result
from utils.app_exceptions import AppException


class UserService(BaseService[UserDAL, UserCreate, UserUpdate]):
    def create(
        self, db: Session, obj_in: UserCreate, pharmacy_in: Optional[PharmacyCreate]
    ):
        if self.dal(self.model).read_one_filtered_by_email(db, obj_in.email):
            return ServiceResult(AppException.BadRequest("This email is already taken"))
        if self.dal(self.model).read_one_filtered_by_phone(db, obj_in.phone):
            return ServiceResult(AppException.BadRequest("This phone is already taken"))
        db_obj = obj_in.dict(exclude={"password"})
        password = get_password_hash(obj_in.password)
        db_obj.update({"password": password, "is_active": False})
        if pharmacy_in:
            if pharmacy_service.get_one_by_trade_license(
                db, trade_license=pharmacy_in.trade_license
            ):
                return ServiceResult(
                    AppException.BadRequest("This trade license is already taken")
                )
            user = self.dal(self.model).create_without_commit_but_flush(
                db, obj_in=UserInDB(**db_obj)
            )
            if pharmacy_service.create_along_with_user(
                db, obj_in=pharmacy_in, user_id=user.id
            ):
                return ServiceResult(
                    self.dal(self.model).just_commit_and_return_db_obj(db, db_obj=user),
                    status_code=status.HTTP_201_CREATED,
                )
        else:
            # return super().create(
            #     db, obj_in=UserInDB(**db_obj)
            # )  # after modify had to unwrap as dal works with object-type BaseModel
            return self.dal(self.model).create_with_commit(
                db, obj_in=UserInDB(**db_obj)
            )

    def get_many(self, db: Session, current_user: User, skip: int = 0, limit: int = 10):
        """checking superuser"""
        role = role_service.get_one_by_id(db, id=current_user.role_id)
        if (handle_result(role).name) != "superuser":
            return ServiceResult(
                AppException.CredentialsException("Not permittable for pharmacy user")
            )
        data = self.dal(self.model).read_many_offset_limit(
            db,
            skip=skip,
            limit=limit,
        )
        if not data:
            return ServiceResult(
                AppException.NotFound(f"No {self.model.__name__.lower()}s found")
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

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

    def get_one_by_id(self, db: Session, id: int):
        data = self.dal(self.model).read_one_filtered_by_id(db, id)
        if not data:
            return ServiceResult(
                AppException.NotFound(
                    f"No {self.model.__name__.lower()} found with this id: {id}"
                )
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

    def activate_user(self, db: Session, current_user: User, id: int):
        """checking superuser"""
        role = role_service.get_one_by_id(db, id=current_user.role_id)
        if (handle_result(role).name) != "superuser":
            return ServiceResult(
                AppException.CredentialsException("Not permittable for pharmacy user")
            )
        user = self.dal(self.model).update_one_filtered_by_id_to_activate_user(db, id)
        if not user:
            return ServiceResult(AppException.NotAccepted())
        return ServiceResult(user, status_code=status.HTTP_202_ACCEPTED)


user_service = UserService(UserDAL, User)
