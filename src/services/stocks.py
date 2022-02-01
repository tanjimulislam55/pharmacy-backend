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


stock_service = StockService(StockDAL, Stock)
