from sqlalchemy.orm import Session

from .base import BaseDAL
from src.models import PurchaseOrder, PurchaseOrderLine
from src.schemas import (
    PurchaseOrderCreate,
    PurchaseOrderLineCreate,
    PurchaseOrderUpdate,
)


class PurchaseOrderDAL(
    BaseDAL[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]
):
    pass


class PurchaseOrderLineDAL(BaseDAL[PurchaseOrderLine, PurchaseOrderLineCreate, None]):
    def create_without_commit_but_flush(
        self, db: Session, obj_in: PurchaseOrderLineCreate, purchase_order_id: int
    ) -> PurchaseOrderLine:
        db_obj = self.model(**obj_in.dict(), purchase_id=purchase_order_id)
        db.add(db_obj)
        db.flush()
        return db_obj
