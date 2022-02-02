from sqlalchemy.orm import Session

from .base import BaseDAL
from src.models import InvoiceOrder, InvoiceOrderLine
from src.schemas import (
    InvoiceOrderCreate,
    InvoiceOrderLineCreate,
    InvoiceOrderUpdate,
)


class InvoiceOrderDAL(BaseDAL[InvoiceOrder, InvoiceOrderCreate, InvoiceOrderUpdate]):
    pass


class InvoiceOrderLineDAL(BaseDAL[InvoiceOrderLine, InvoiceOrderLineCreate, None]):
    def create_without_commit_but_flush(
        self, db: Session, obj_in: InvoiceOrderLineCreate, invoice_order_id: int
    ) -> InvoiceOrderLine:
        db_obj = self.model(**obj_in.dict(), invoice_id=invoice_order_id)
        db.add(db_obj)
        db.flush()
        return db_obj
