from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import (
    PurchaseOrderOut,
    PurchaseOrderLineCreate,
    PurchaseOrderCreate,
)
from src.models import User
from src.services import purchase_order_service
from src.utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=PurchaseOrderOut)
def create_new_purchase_order(
    purchase_order_in: PurchaseOrderCreate,
    purchase_order_line_in: List[PurchaseOrderLineCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    purchase_order = purchase_order_service.create_along_with_purchase_lines(
        db,
        obj_in_for_purchase_order=purchase_order_in,
        obj_in_for_purchase_order_lines=purchase_order_line_in,
    )
    return handle_result(purchase_order)


@router.get("/", response_model=List[PurchaseOrderOut])
def get_all_purchase_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    purchase_orders = purchase_order_service.get_many(db, skip=skip, limit=limit)
    return handle_result(purchase_orders)


"""if need to update purchase order must update trade. Pending until then"""
# @router.put("/{purchase_order_id}", response_model=PurchaseOrderOut)
# def update_purchase_order_by_id(
#     purchase_order_id: int,
#     purchase_order_update: PurchaseOrderUpdate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user),
# ):
#     purchase_order = purchase_order_service.update_by_id(
#         db, id=purchase_order_id, obj_in=purchase_order_update
#     )
#     return handle_result(purchase_order)
