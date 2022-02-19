from sqlalchemy.orm import Session
from typing import Optional

from .base import BaseDAL
from models import Stock
from schemas import StockCreate, StockUpdate


class StockDAL(BaseDAL[Stock, StockCreate, StockUpdate]):
    def increase_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, medicine_id: int, quantity: int
    ) -> Stock:
        db.query(self.model).filter(self.model.medicine_id == medicine_id).update(
            {self.model.in_stock: self.model.in_stock + quantity},
            synchronize_session=False,
        )

    def decrease_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, medicine_id: int, quantity: int
    ) -> Stock:
        db.query(self.model).filter(self.model.medicine_id == medicine_id).update(
            {self.model.in_stock: self.model.in_stock - quantity},
            synchronize_session=False,
        )

    def read_one_filtered_by_medicine_id(
        self, db: Session, medicine_id: int
    ) -> Optional[Stock]:
        return (
            db.query(self.model).filter(self.model.medicine_id == medicine_id).first()
        )

    def update_one_filtered_by_medicine_id(
        self, db: Session, medicine_id: int, obj_in: StockUpdate
    ) -> Stock:
        db.query(self.model).filter(self.model.medicine_id == medicine_id).update(
            obj_in.dict(exclude_unset=True), synchronize_session=False
        )

    def update_one_filtered_by_medicine_id_with_commit(
        self, db: Session, medicine_id: int, obj_in: StockUpdate
    ) -> Stock:
        db.query(self.model).filter(self.model.medicine_id == medicine_id).update(
            obj_in.dict(exclude_unset=True), synchronize_session=False
        )
        db.commit()
        return self.read_one_filtered_by_medicine_id(db, medicine_id)
