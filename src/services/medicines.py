from sqlalchemy.orm import Session
from fastapi import status
from typing import Optional

from .base import BaseService
from src.dals import MedicineDAL
from src.models import Medicine
from src.schemas import MedicineCreate, MedicineUpdate, StockCreate
from .stocks import stock_service
from src.utils.service_result import ServiceResult
from src.utils.app_exceptions import AppException


class MedicineService(BaseService[MedicineDAL, MedicineCreate, MedicineUpdate]):
    def create_along_with_stock(self, db: Session, obj_in: MedicineCreate):
        medicine = self.dal(self.model).create_without_commit_but_flush(db, obj_in)
        if not medicine:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding medicine")
            )
        stock_data: dict = {"medicine_id": medicine.id}
        stock_in = StockCreate(**stock_data)
        if stock_service.create_along_with_medicine(db, obj_in=stock_in):
            data = self.dal(self.model).just_commit_and_return_db_obj(
                db, db_obj=medicine
            )
            if not data:
                return ServiceResult(
                    AppException.ServerError("Problem while commiting")
                )
            return ServiceResult(data, status_code=status.HTTP_201_CREATED)

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


medicine_service = MedicineService(MedicineDAL, Medicine)
