from fastapi import status
from sqlalchemy.orm import Session

from schemas import RoleCreate, RoleUpdate
from models import Role, User
from .base import BaseService
from dals import RoleDAL
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult, handle_result


class RoleService(BaseService[RoleDAL, RoleCreate, RoleUpdate]):
    def create(self, db: Session, obj_in: RoleCreate):
        data = self.dal(self.model).create_with_commit(db, obj_in)
        if not data:
            return ServiceResult(AppException.ServerError("Something went wrong"))
        return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    def get_many(self, db: Session, current_user: User, skip: int = 0, limit: int = 10):
        role = self.get_one_by_id(db, id=current_user.role_id)
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

    def get_one_by_id(self, db: Session, id: int):
        data = self.dal(self.model).read_one_filtered_by_id(db, id)
        if not data:
            return ServiceResult(
                AppException.NotFound(
                    f"No {self.model.__name__.lower()} found with this id: {id}"
                )
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def update_by_id(
        self, db: Session, current_user: User, id: int, obj_in: RoleUpdate
    ):
        role = self.get_one_by_id(db, id=current_user.role_id)
        if (handle_result(role).name) != "superuser":
            return ServiceResult(
                AppException.CredentialsException("Not permittable for pharmacy user")
            )
        data = self.dal(self.model).update_one_filtered_by_id(db, id, obj_in)
        if not data:
            return ServiceResult(AppException.NotAccepted())
        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)


role_service = RoleService(RoleDAL, Role)
