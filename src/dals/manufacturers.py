from sqlalchemy.orm import Session
from typing import Optional, List

from .base import BaseDAL
from models import Manufacturer, Trade, TradeHistory
from schemas import (
    ManufacturerCreate,
    ManufacturerUpdate,
    TradeCreate,
    TradeUpdate,
    TradeHistoryCreate,
    TradeHistoryUpdate,
)


class ManufacturerDAL(BaseDAL[Manufacturer, ManufacturerCreate, ManufacturerUpdate]):
    def create_with_commit(
        self, db: Session, obj_in: ManufacturerCreate
    ) -> Manufacturer:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_one_filtered_by_manufacturer_name(
        self, db: Session, manufacturer_name: str
    ) -> Optional[Manufacturer]:
        return db.query(self.model).filter(self.model.name == manufacturer_name).first()

    def read_many_offset_limit(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Manufacturer]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def read_one_filtered_by_id(self, db: Session, id: int) -> Optional[Manufacturer]:
        return db.query(self.model).filter(self.model.id == id).first()


class TradeDAL(BaseDAL[Trade, TradeCreate, TradeUpdate]):
    def create_with_commit(
        self, db: Session, obj_in: TradeCreate, manufacturer_id: int, pharmacy_id: int
    ) -> Trade:
        db_obj = self.model(
            **obj_in.dict(), manufacturer_id=manufacturer_id, pharmacy_id=pharmacy_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_one_filtered_by_manufacturer_id_without_commit(
        self, db: Session, obj_in: TradeUpdate, manufacturer_id: int, pharmacy_id: int
    ) -> Trade:
        db.query(self.model).filter(
            self.model.manufacturer_id == manufacturer_id,
            self.model.pharmacy_id == pharmacy_id,
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
        self, db: Session, manufacturer_id: int, pharmacy_id: int
    ) -> Optional[Trade]:
        return (
            db.query(self.model)
            .filter(
                self.model.manufacturer_id == manufacturer_id,
                self.model.pharmacy_id == pharmacy_id,
            )
            .first()
        )


class TradeHistoryDAL(BaseDAL[TradeHistory, TradeHistoryCreate, TradeHistoryUpdate]):
    def create_with_commit(
        self,
        db: Session,
        obj_in: TradeHistoryCreate,
        manufacturer_id: int,
        pharmacy_id: int,
    ) -> Trade:
        db_obj = self.model(
            **obj_in.dict(), manufacturer_id=manufacturer_id, pharmacy_id=pharmacy_id
        )
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
