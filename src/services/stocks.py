from sqlalchemy.orm import Session
from fastapi import status

from .base import BaseService
from dals import StockDAL
from models import Stock, User
from schemas import StockCreate, StockUpdate
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult


class StockService(BaseService[StockDAL, StockCreate, StockUpdate]):
    def create(self, db: Session, current_user: User, medicine_id: int):
        stock = self.dal(self.model).create_with_commit(
            db,
            obj_in=StockCreate(medicine_id=medicine_id),
            pharmacy_id=current_user.pharmacy.id,
        )
        if not stock:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding stock")
            )
        return stock

    def get_one_by_pharmacy_id(self, db: Session, current_user: User, medicine_id: int):
        data = self.dal(self.model).read_one_filtered_by_medicine_id(
            db, medicine_id, pharmacy_id=current_user.pharmacy.id
        )
        return data

    def available_quantity(
        self, db: Session, current_user: User, id: int, quantity: int
    ) -> int:
        stock = self.dal(self.model).read_one_filtered_by_medicine_id(
            db, id, pharmacy_id=current_user.pharmacy.id
        )
        return stock.in_stock

    def increase_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, current_user: User, medicine_id: int, quantity: int
    ):
        stock = self.dal(
            self.model
        ).increase_stock_quantity_filtered_by_medicine_id_without_commit(
            db, medicine_id, quantity, pharmacy_id=current_user.pharmacy.id
        )
        if not stock:
            return ServiceResult(
                AppException.ServerError(
                    "Problem occured while increasing medicine stock"
                )
            )
        return stock

    def decrease_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, current_user: User, medicine_id: int, quantity: int
    ):
        stock = self.dal(
            self.model
        ).decrease_stock_quantity_filtered_by_medicine_id_without_commit(
            db, medicine_id, quantity, pharmacy_id=current_user.pharmacy.id
        )
        if not stock:
            return ServiceResult(
                AppException.ServerError(
                    "Problem occured while decreasing medicine stock"
                )
            )
        return stock

    def update_filtered_by_medicine_id(
        self, db: Session, current_user: User, medicine_id: int, obj_in: StockUpdate
    ):
        stock = self.dal(self.model).update_one_filtered_by_medicine_id(
            db, medicine_id, obj_in, pharmacy_id=current_user.pharmacy.id
        )
        if not stock:
            return ServiceResult(AppException.NotAccepted("Could not update stock"))
        return stock

    def update_filtered_by_medicine_id_with_commit(
        self, db: Session, current_user: User, medicine_id: int, obj_in: StockUpdate
    ):
        stock = self.dal(self.model).update_one_filtered_by_medicine_id_with_commit(
            db, medicine_id, obj_in, pharmacy_id=current_user.pharmacy.id
        )
        if not stock:
            return ServiceResult(AppException.NotAccepted("Could not update stock"))
        return stock

    def get_sum_of_in_stock_values_filtered_by_datetime(
        self, db: Session, current_user: User
    ) -> int:
        data = self.dal(self.model).read_all(db, pharmacy_id=current_user.pharmacy.id)
        sum: int = 0
        if not data:
            return ServiceResult(sum, status_code=status.HTTP_204_NO_CONTENT)
        for item in data:
            sum += item.in_stock
        return ServiceResult(sum, status_code=status.HTTP_200_OK)


stock_service = StockService(StockDAL, Stock)
