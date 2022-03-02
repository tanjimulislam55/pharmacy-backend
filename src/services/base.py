from typing import Generic, Type, TypeVar, Optional
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from db.config import Base
from models import User
from dals.base import BaseDAL
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelDAL = TypeVar("ModelDAL", bound=BaseDAL)


class BaseService(Generic[ModelDAL, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, dal: Type[ModelDAL], model: Type[ModelType]):
        self.dal = dal
        self.model = model

    def create(self, db: Session, current_user: User, obj_in: CreateSchemaType):
        data = self.dal(self.model).create_with_commit(
            db, obj_in=obj_in, pharmacy_id=current_user.pharmacy.id
        )
        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong"))
        return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    def get_one_by_id(self, db: Session, current_user: User, id: int):
        data = self.dal(self.model).read_one_filtered_by_id(
            db, id, pharmacy_id=current_user.pharmacy.id
        )
        if not data:
            return ServiceResult(
                AppException.NotFound(
                    f"No {self.model.__name__.lower()} found with this id: {id}"
                )
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_many(self, db: Session, current_user: User, skip: int = 0, limit: int = 10):
        data = self.dal(self.model).read_many_offset_limit(
            db,
            pharmacy_id=current_user.pharmacy.id,
            skip=skip,
            limit=limit,
        )
        # if not data:
        #     return ServiceResult(
        #         AppException.NotFound(f"No {self.model.__name__.lower()}s found")
        #     )
        #     return ServiceResult(data, status_code=status.HTTP_404_NOT_FOUND)
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_many_filtered_by_datetime(
        self,
        db: Session,
        current_user: User,
        from_datetime: Optional[datetime],
        till_datetime: Optional[datetime],
        skip: int = 0,
        limit: int = 10,
    ):
        data = self.dal(self.model).read_many_offset_limit_filtered_by_datetime(
            db,
            from_datetime,
            till_datetime,
            pharmacy_id=current_user.pharmacy.id,
            skip=skip,
            limit=limit,
        )
        if not data:
            return ServiceResult(
                AppException.NotFound(f"No {self.model.__name__.lower()}s found")
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def update_by_id(
        self, db: Session, current_user: User, id: int, obj_in: UpdateSchemaType
    ):
        data = self.dal(self.model).update_one_filtered_by_id(
            db, id, obj_in, pharmacy_id=current_user.pharmacy.id
        )
        if not data:
            return ServiceResult(AppException.NotAccepted())
        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)

    def remove_by_id(self, db: Session, current_user: User, id: int):
        return (
            ServiceResult("Deleted", status_code=status.HTTP_202_ACCEPTED)
            if self.dal(self.model).delete_one_filtered_by_id(
                db, id, pharmacy_id=current_user.pharmacy.id
            )
            else ServiceResult(AppException.Forbidden())
        )
