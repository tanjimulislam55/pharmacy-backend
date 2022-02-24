from sqlalchemy.orm import Session
from fastapi import status
from typing import Optional

from .base import BaseService
from dals import MedicineDAL
from models import Medicine, User
from schemas import MedicineCreate, MedicineUpdate
from .roles import role_service
from utils.service_result import ServiceResult, handle_result
from utils.app_exceptions import AppException


class MedicineService(BaseService[MedicineDAL, MedicineCreate, MedicineUpdate]):
    def create(self, db: Session, current_user: User, obj_in: MedicineCreate):
        """checking superuser"""
        role = role_service.get_one_by_id(db, id=current_user.role_id)
        if (handle_result(role).name) != "superuser":
            return ServiceResult(
                AppException.CredentialsException("Not permittable for pharmacy user")
            )
        medicine = self.dal(self.model).create_with_commit(db, obj_in)
        if not medicine:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding medicine")
            )
        return ServiceResult(medicine, status_code=status.HTTP_201_CREATED)

    def get_many(self, db: Session, skip: int = 0, limit: int = 10):
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

    def update_by_id(self, db: Session, id: int, obj_in: MedicineUpdate):
        data = self.dal(self.model).update_one_filtered_by_id(db, id, obj_in)
        if not data:
            return ServiceResult(AppException.NotAccepted())
        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)

    def get_many_by_brand_name_letters(
        self, db: Session, name_str: Optional[str], skip: int = 0, limit: int = 10
    ):
        data = self.dal(self.model).read_many_filtered_by_brand_name_letters(
            db, name_str, skip, limit
        )
        if not data:
            return ServiceResult([], status_code=status.HTTP_204_NO_CONTENT)
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_many_by_generic_name_letters(
        self, db: Session, name_str: Optional[str], skip: int = 0, limit: int = 10
    ):
        data = self.dal(self.model).read_many_filtered_by_generic_name_letters(
            db, name_str, skip, limit
        )
        if not data:
            return ServiceResult([], status_code=status.HTTP_204_NO_CONTENT)
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_many_by_manufacturer_id(
        self,
        db: Session,
        manufacturer_id: int,
        skip: int = 0,
        limit: int = 10,
    ):
        data = self.dal(self.model).read_many_filtered_by_manufacturer_id(
            db, manufacturer_id, skip, limit
        )
        if not data:
            return ServiceResult([], status_code=status.HTTP_204_NO_CONTENT)
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_many_by_manufacturer_id_and_brand_name_letters(
        self,
        db: Session,
        manufacturer_id: int,
        name_str: Optional[str],
        skip: int = 0,
        limit: int = 10,
    ):
        data = self.dal(
            self.model
        ).read_many_filtered_by_manufacturer_id_and_brand_name(
            db, manufacturer_id, name_str, skip, limit
        )
        if not data:
            return ServiceResult([], status_code=status.HTTP_204_NO_CONTENT)
        return ServiceResult(data, status_code=status.HTTP_200_OK)

    def get_many_join_with_stock(self, db: Session, current_user: User):
        medicines = self.dal(self.model).read_many_join_with_stock(
            db, pharmacy_id=current_user.pharmacy.id
        )
        if not medicines:
            return ServiceResult(AppException.NotFound("No medicines found"))
        return ServiceResult(medicines, status_code=status.HTTP_200_OK)

    def calculate_total_stock_costs(self, db: Session, current_user: User) -> float:
        data = self.get_many_join_with_stock(db, current_user)
        sum: float = 0
        if not data:
            return ServiceResult(sum, status_code=status.HTTP_204_NO_CONTENT)
        for item in handle_result(data):
            sum += item.in_stock * item.unit_price
        return ServiceResult(sum, status_code=status.HTTP_200_OK)


medicine_service = MedicineService(MedicineDAL, Medicine)
