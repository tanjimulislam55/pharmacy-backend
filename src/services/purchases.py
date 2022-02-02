from sqlalchemy.orm import Session
from fastapi import status
from typing import List

from .base import BaseService
from .stocks import stock_service
from src.dals import PurchaseOrderDAL, PurchaseOrderLineDAL
from src.models import PurchaseOrder, PurchaseOrderLine
from src.schemas import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderLineCreate,
)
from src.utils.service_result import ServiceResult
from src.utils.app_exceptions import AppException


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
            # also increasing stock
            stock_service.increase_stock_quantity_filtered_by_medicine_id_without_commit(  # noqa E501
                db,
                medicine_id=every_purchase_order_line.medicine_id,
                quantity=every_purchase_order_line.quantity,
            )

        return True


purchase_order_service = PurchaseOrderService(PurchaseOrderDAL, PurchaseOrder)


purchase_order_line_service = PurchaseOrderLineService(
    PurchaseOrderLineDAL, PurchaseOrderLine
)
