from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import (
    InvoiceOrderCreate,
    InvoiceOrderUpdate,
    InvoiceOrderLineCreate,
    InvoiceOrderOut,
)
from src.models import User
from src.services import invoice_order_service
from src.utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=InvoiceOrderOut)
def create_new_invoice_order(
    invoice_order_in: InvoiceOrderCreate,
    invoice_order_line_in: List[InvoiceOrderLineCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    invoice_order = invoice_order_service.create_along_with_invoice_lines(
        db,
        obj_in_for_invoice_order=invoice_order_in,
        obj_in_for_invoice_order_lines=invoice_order_line_in,
    )
    return handle_result(invoice_order)


@router.get("/", response_model=List[InvoiceOrderOut])
def get_all_invoice_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    invoice_orders = invoice_order_service.get_many(db, skip=skip, limit=limit)
    return handle_result(invoice_orders)


@router.put("/{invoice_order_id}", response_model=InvoiceOrderUpdate)
def update_invoice_order_by_id(
    invoice_order_id: int,
    invoice_order_update: InvoiceOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    invoice_order = invoice_order_service.update_by_id(
        db, id=invoice_order_id, obj_in=invoice_order_update
    )
    return handle_result(invoice_order)
