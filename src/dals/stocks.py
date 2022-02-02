from sqlalchemy.orm import Session
from typing import Optional

from .base import BaseDAL
from src.models import Stock
from src.schemas import StockCreate, StockUpdate


class StockDAL(BaseDAL[Stock, StockCreate, StockUpdate]):
    def update_specific_stock_attributes_filtered_by_medicine_id_without_commit(
        self, db: Session, medicine_id: int, obj_in: StockUpdate
    ) -> Stock:
        db.query(self.model).filter(self.model.medicine_id == medicine_id).update(
            # here obj_in.in_stock is actually decreaseable quantity from stock
            {
                **obj_in.dict(exclude={"in_stock"}),
                **{self.model.in_stock: self.model.in_stock - obj_in.in_stock},
            },
            synchronize_session=False,
        )
        return self.read_one_filtered_by_medicine_id(db, medicine_id=medicine_id)

    def increase_stock_quantity_filtered_by_medicine_id_without_commit(
        self, db: Session, medicine_id: int, quantity: int
    ) -> Stock:
        db.query(self.model).filter(self.model.medicine_id == medicine_id).update(
            {self.model.in_stock: self.model.in_stock + quantity},
            synchronize_session=False,
        )
        return self.read_one_filtered_by_medicine_id(db, medicine_id=medicine_id)

    def read_one_filtered_by_medicine_id(
        self, db: Session, medicine_id: int
    ) -> Optional[Stock]:
        return (
            db.query(self.model).filter(self.model.medicine_id == medicine_id).first()
        )
