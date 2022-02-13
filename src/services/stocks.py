from sqlalchemy.orm import Session

from .base import BaseService
from src.dals import StockDAL
from src.models import Stock
from src.schemas import StockCreate, StockUpdate
from src.utils.app_exceptions import AppException
from src.utils.service_result import ServiceResult


class StockService(BaseService[StockDAL, StockCreate, StockUpdate]):
    def create_along_with_medicine(self, db: Session, obj_in: StockCreate):
        stock = self.dal(self.model).create_without_commit_but_flush(db, obj_in)
        if not stock:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding stock")
            )
        return stock

    def available_quantity(self, db: Session, id: int, quantity: int) -> int:
        stock = self.dal(self.model).read_one_filtered_by_medicine_id(db, id)
        return stock.in_stock

    def increase_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, medicine_id: int, quantity: int
    ):
        stock = self.dal(
            self.model
        ).increase_stock_quantity_filtered_by_medicine_id_without_commit(
            db, medicine_id, quantity
        )
        if not stock:
            return ServiceResult(
                AppException.ServerError(
                    "Problem occured while increasing medicine stock"
                )
            )
        return stock

    def decrease_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, medicine_id: int, quantity: int
    ):
        stock = self.dal(
            self.model
        ).decrease_stock_quantity_filtered_by_medicine_id_without_commit(
            db, medicine_id, quantity
        )
        if not stock:
            return ServiceResult(
                AppException.ServerError(
                    "Problem occured while decreasing medicine stock"
                )
            )
        return stock

    def update_filtered_by_medicine_id(
        self, db: Session, medicine_id: int, obj_in: StockUpdate
    ):
        stock = self.dal(self.model).update_one_filtered_by_medicine_id(
            self, db, medicine_id, obj_in
        )
        if not stock:
            return ServiceResult(AppException.NotAccepted("Could not update stock"))
        return stock


stock_service = StockService(StockDAL, Stock)
