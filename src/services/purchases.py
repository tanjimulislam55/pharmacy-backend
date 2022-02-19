from sqlalchemy.orm import Session
from fastapi import status
from typing import List

from .base import BaseService
from dals import PurchaseOrderDAL, PurchaseOrderLineDAL
from models import PurchaseOrder, PurchaseOrderLine
from schemas import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderLineCreate,
    TradeUpdate,
)
from .manufacturers import trade_service
from utils.service_result import ServiceResult
from utils.app_exceptions import AppException


class PurchaseOrderService(
    BaseService[PurchaseOrderDAL, PurchaseOrderCreate, PurchaseOrderUpdate]
):
    def create_along_with_purchase_lines(
        self,
        db: Session,
        obj_in_for_purchase_order: PurchaseOrderCreate,
        obj_in_for_purchase_order_lines: List[PurchaseOrderLineCreate],
    ):
        purchase_order = self.dal(self.model).create_without_commit_but_flush(
            db, obj_in_for_purchase_order
        )
        if not purchase_order:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding purchase order")
            )
        if purchase_order_line_service.create_along_with_purchase_order(
            db,
            obj_in=obj_in_for_purchase_order_lines,
            purchase_order_id=purchase_order.id,
        ):
            """also updating trade"""
            trade_service.update_by_manufacturer_id_while_processing_purchase_order(
                db,
                manufacturer_id=purchase_order.manufacturer_id,
                obj_in=TradeUpdate(
                    closing_balance=purchase_order.paid_amount,
                    outstanding_amount=purchase_order.due_amount,
                ),
            )
            """finally commiting"""
            data = self.dal(self.model).just_commit_and_return_db_obj(
                db, db_obj=purchase_order
            )
            if not data:
                return ServiceResult(
                    AppException.ServerError("Problem while commiting")
                )
            return ServiceResult(data, status_code=status.HTTP_201_CREATED)


class PurchaseOrderLineService(
    BaseService[PurchaseOrderLineDAL, PurchaseOrderLineCreate, None]
):
    def create_along_with_purchase_order(
        self, db: Session, obj_in: List[PurchaseOrderLineCreate], purchase_order_id: int
    ):
        for every_purchase_order_line in obj_in:
            purchase_order_line = self.dal(self.model).create_without_commit_but_flush(
                db,
                obj_in=every_purchase_order_line,
                purchase_order_id=purchase_order_id,
            )
            if not purchase_order_line:
                return ServiceResult(
                    AppException.ServerError(
                        "Problem occured while adding purchase order lines"
                    )
                )

        return True


purchase_order_service = PurchaseOrderService(PurchaseOrderDAL, PurchaseOrder)


purchase_order_line_service = PurchaseOrderLineService(
    PurchaseOrderLineDAL, PurchaseOrderLine
)
