from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from api.deps import get_current_active_user, get_db
from schemas import (
    InvoiceOrderCreate,
    InvoiceOrderUpdate,
    InvoiceOrderLineCreate,
    InvoiceOrderOut,
)
from models import User
from services import invoice_order_service
from utils.service_result import handle_result

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


@router.get("/filtered_by_datetime/", response_model=List[InvoiceOrderOut])
def get_all_invoice_orders_filtered_by_datetime(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    from_datetime: Optional[datetime] = datetime.strptime(
        "2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
    ),
    till_datetime: Optional[datetime] = str(datetime.now()),
):
    invoice_orders = invoice_order_service.get_many_filtered_by_datetime(
        db,
        from_datetime=from_datetime,
        till_datetime=till_datetime,
        skip=skip,
        limit=limit,
    )
    return handle_result(invoice_orders)


@router.get("/get_sum_filtered_by_datetime/")
def get_sum_filtered_by_datetime(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    from_datetime: Optional[datetime] = datetime.strptime(
        "2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
    ),
    till_datetime: Optional[datetime] = str(datetime.now()),
):
    value = invoice_order_service.get_sum_of_values_for_specific_column_filtered_by_datetime(  # noqa E501
        db,
        from_datetime=from_datetime,
        till_datetime=till_datetime,
    )
    return handle_result(value)


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
