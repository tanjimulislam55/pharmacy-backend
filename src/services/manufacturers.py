from sqlalchemy.orm import Session
from fastapi import status

from .base import BaseService
from dals import ManufacturerDAL, TradeDAL, TradeHistoryDAL
from models import Manufacturer, Trade, TradeHistory, User
from .roles import role_service
from schemas import (
    ManufacturerCreate,
    ManufacturerUpdate,
    TradeCreate,
    TradeUpdate,
    TradeHistoryCreate,
    TradeHistoryUpdate,
)
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult, handle_result


class ManufacturerService(
    BaseService[ManufacturerDAL, ManufacturerCreate, ManufacturerUpdate]
):
    def create(self, db: Session, current_user: User, obj_in: ManufacturerCreate):
        """checking superuser"""
        role = role_service.get_one_by_id(db, id=current_user.role_id)
        if (handle_result(role).name) != "superuser":
            return ServiceResult(
                AppException.CredentialsException("Not permittable for pharmacy user")
            )
        if self.dal(self.model).read_one_filtered_by_manufacturer_name(
            db, manufacturer_name=obj_in.name
        ):
            return ServiceResult(AppException.NotAccepted("This name is already taken"))
        manufacturer = self.dal(self.model).create_with_commit(db, obj_in)
        if not manufacturer:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding manufacturer")
            )
        return ServiceResult(manufacturer, status_code=status.HTTP_201_CREATED)

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


class TradeService(BaseService[TradeDAL, TradeCreate, TradeUpdate]):
    def create(self, db: Session, current_user: User, manufacturer_id: int):
        trade = self.dal(self.model).create_with_commit(
            db,
            obj_in=TradeCreate(),
            manufacturer_id=manufacturer_id,
            pharmacy_id=current_user.pharmacy.id,
        )
        if not trade:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding trade")
            )
        # return True
        return trade

    def get_one_by_pharmacy_id(
        self, db: Session, current_user: User, manufacturer_id: int
    ):
        data = self.dal(self.model).read_one_filtered_by_manufacturer_id(
            db, manufacturer_id, pharmacy_id=current_user.pharmacy.id
        )
        return data

    def update_by_manufacturer_id_while_processing_purchase_order(
        self, db: Session, current_user: User, manufacturer_id: int, obj_in: TradeUpdate
    ):
        if (
            self.dal(self.model).update_one_filtered_by_manufacturer_id_without_commit(
                db, obj_in, manufacturer_id, pharmacy_id=current_user.pharmacy.id
            )
            == 0
        ):
            return ServiceResult(AppException.NotAccepted())


class TradeHistoryService(
    BaseService[TradeHistoryDAL, TradeHistoryCreate, TradeHistoryUpdate]
):
    def create_along_with_grn(
        self, db: Session, current_user: User, manufacturer_id: int, amount: float
    ):
        trade_history = self.dal(self.model).create_with_commit(
            db,
            obj_in=TradeHistoryCreate(purchased_amount=amount),
            manufacturer_id=manufacturer_id,
            pharmacy_id=current_user.pharmacy.id,
        )
        if not trade_history:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding trade histories")
            )
        return True


manufacturer_service = ManufacturerService(ManufacturerDAL, Manufacturer)
trade_service = TradeService(TradeDAL, Trade)
trade_history_service = TradeHistoryService(TradeHistoryDAL, TradeHistory)
