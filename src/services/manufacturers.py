from sqlalchemy.orm import Session
from fastapi import status

from .base import BaseService
from dals import ManufacturerDAL, TradeDAL, TradeHistoryDAL
from models import Manufacturer, Trade, TradeHistory
from schemas import (
    ManufacturerCreate,
    ManufacturerUpdate,
    TradeCreate,
    TradeUpdate,
    TradeHistoryCreate,
    TradeHistoryUpdate,
)
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult


class ManufacturerService(
    BaseService[ManufacturerDAL, ManufacturerCreate, ManufacturerUpdate]
):
    def create_along_with_trade(self, db: Session, obj_in: ManufacturerCreate):
        if self.dal(self.model).read_one_filtered_by_manufacturer_name(
            db, manufacturer_name=obj_in.name
        ):
            return ServiceResult(AppException.NotAccepted("This name is already taken"))
        manufacturer = self.dal(self.model).create_without_commit_but_flush(db, obj_in)
        if not manufacturer:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding manufacturer")
            )

        if trade_service.create_along_with_manufacturer(
            db, manufacturer_id=manufacturer.id
        ):
            data = self.dal(self.model).just_commit_and_return_db_obj(
                db, db_obj=manufacturer
            )
            if not data:
                return ServiceResult(
                    AppException.ServerError("Problem while commiting")
                )
            return ServiceResult(data, status_code=status.HTTP_201_CREATED)


class TradeService(BaseService[TradeDAL, TradeCreate, TradeUpdate]):
    def create_along_with_manufacturer(self, db: Session, manufacturer_id: int):
        trade = self.dal(self.model).create_without_commit_but_flush(
            db, obj_in=TradeCreate(), manufacturer_id=manufacturer_id
        )
        if not trade:
            return ServiceResult(
                AppException.ServerError(
                    "Problem occured while adding purchase order lines"
                )
            )
        return True

    def update_by_manufacturer_id_while_processing_purchase_order(
        self, db: Session, manufacturer_id: int, obj_in: TradeUpdate
    ):
        data = self.dal(
            self.model
        ).update_one_filtered_by_manufacturer_id_without_commit(
            db, obj_in, manufacturer_id
        )
        if not data:
            return ServiceResult(AppException.NotAccepted())
        return ServiceResult(data, status_code=status.HTTP_202_ACCEPTED)


class TradeHistoryService(
    BaseService[TradeHistoryDAL, TradeHistoryCreate, TradeHistoryUpdate]
):
    def create_along_with_grn(self, db: Session, manufacturer_id: int, amount: float):
        trade_history = self.dal(self.model).create_with_commit(
            db,
            obj_in=TradeHistoryCreate(purchased_amount=amount),
            manufacturer_id=manufacturer_id,
        )
        if not trade_history:
            return ServiceResult(
                AppException.ServerError(
                    "Problem occured while adding purchase order lines"
                )
            )
        return True


manufacturer_service = ManufacturerService(ManufacturerDAL, Manufacturer)
trade_service = TradeService(TradeDAL, Trade)
trade_history_service = TradeHistoryService(TradeHistoryDAL, TradeHistory)
