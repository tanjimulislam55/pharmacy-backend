from fastapi import status
from sqlalchemy.orm import Session

from schemas import RoleCreate, RoleUpdate
from models import Role
from .base import BaseService
from dals import RoleDAL
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult


class RoleService(BaseService[RoleDAL, RoleCreate, RoleUpdate]):
    def get_one_by_id(self, db: Session, id: int):
        data = self.dal(self.model).read_one_filtered_by_id(db, id)
        if not data:
            return ServiceResult(
                AppException.NotFound(
                    f"No {self.model.__name__.lower()} found with this id: {id}"
                )
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)


role_service = RoleService(RoleDAL, Role)
