from sqlalchemy.orm import Session
from typing import Optional

from .base import BaseDAL
from src.models import Manufacturer, Trade, TradeHistory
from src.schemas import (
    ManufacturerCreate,
    ManufacturerUpdate,
    TradeCreate,
    TradeUpdate,
    TradeHistoryCreate,
    TradeHistoryUpdate,
)


class ManufacturerDAL(BaseDAL[Manufacturer, ManufacturerCreate, ManufacturerUpdate]):
    def read_one_filtered_by_manufacturer_name(
        self, db: Session, manufacturer_name: str
    ) -> Optional[Manufacturer]:
        return db.query(self.model).filter(self.model.name == manufacturer_name).first()


class TradeDAL(BaseDAL[Trade, TradeCreate, TradeUpdate]):
    def create_without_commit_but_flush(
        self, db: Session, obj_in: TradeCreate, manufacturer_id: int
    ) -> Trade:
        db_obj = self.model(**obj_in.dict(), manufacturer_id=manufacturer_id)
        db.add(db_obj)
        db.flush()
        return db_obj

    def update_one_filtered_by_manufacturer_id_without_commit(
        self, db: Session, obj_in: TradeUpdate, manufacturer_id: int
    ) -> Trade:
        db.query(self.model).filter(
            self.model.manufacturer_id == manufacturer_id
        ).update(
            {
                self.model.closing_balance: self.model.closing_balance
                + obj_in.closing_balance,
                self.model.outstanding_amount: self.model.outstanding_amount
                + obj_in.outstanding_amount,
            },
            synchronize_session=False,
        )

    def read_one_filtered_by_manufacturer_id(
        self, db: Session, manufacturer_id: int
    ) -> Optional[Trade]:
        return (
            db.query(self.model)
            .filter(self.model.manufacturer_id == manufacturer_id)
            .first()
        )


class TradeHistoryDAL(BaseDAL[TradeHistory, TradeHistoryCreate, TradeHistoryUpdate]):
    def create_with_commit(
        self, db: Session, obj_in: TradeHistoryCreate, manufacturer_id: int
    ) -> Trade:
        db_obj = self.model(**obj_in.dict(), manufacturer_id=manufacturer_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def update_specific_stock_attributes_filtered_by_manufacturer_id_without_commit(
    #     self, db: Session, manufacturer_id: int, obj_in: TradeHistoryUpdate
    # ) -> Manufacturer:
    #     db.query(self.model).filter(
    #         self.model.manufacturer_id == manufacturer_id
    #     ).update(
    #         # here obj_in.in_stock is actually decreaseable quantity from stock
    #         {
    #             **obj_in.dict(exclude={"in_stock"}),
    #             **{self.model.in_stock: self.model.in_stock - obj_in.in_stock},
    #         },
    #         synchronize_session=False,
    #     )
    #     return self.read_one_filtered_by_(db, manufacturer_id=manufacturer_id)
