from sqlalchemy.orm import Session
from fastapi import status
from typing import List, Optional
from datetime import datetime

from .base import BaseService
from .stocks import stock_service
from dals import InvoiceOrderDAL, InvoiceOrderLineDAL
from models import InvoiceOrder, InvoiceOrderLine, User
from schemas import (
    InvoiceOrderCreate,
    InvoiceOrderUpdate,
    InvoiceOrderLineCreate,
)
from utils.service_result import ServiceResult
from utils.app_exceptions import AppException


class InvoiceOrderService(
    BaseService[InvoiceOrderDAL, InvoiceOrderCreate, InvoiceOrderUpdate]
):
    def create_along_with_invoice_lines(
        self,
        db: Session,
        current_user: User,
        obj_in_for_invoice_order: InvoiceOrderCreate,
        obj_in_for_invoice_order_lines: List[InvoiceOrderLineCreate],
    ):
        """initially checking for stock availability"""
        for every_invoice_order_line in obj_in_for_invoice_order_lines:
            available_quantity = stock_service.available_quantity(
                db,
                current_user,
                id=every_invoice_order_line.medicine_id,
                quantity=every_invoice_order_line.quantity,
            )
            if not available_quantity > every_invoice_order_line.quantity:
                return ServiceResult(AppException.NotAccepted("Not enough stock"))

        invoice_order = self.dal(self.model).create_without_commit_but_flush(
            db, obj_in=obj_in_for_invoice_order, pharmacy_id=current_user.pharmacy.id
        )
        if not invoice_order:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding invoice order")
            )
        if invoice_order_line_service.create_along_with_invoice_order(
            db,
            current_user,
            obj_in=obj_in_for_invoice_order_lines,
            invoice_order_id=invoice_order.id,
        ):
            data = self.dal(self.model).just_commit_and_return_db_obj(
                db, db_obj=invoice_order
            )
            if not data:
                return ServiceResult(
                    AppException.ServerError("Problem while commiting")
                )
            return ServiceResult(data, status_code=status.HTTP_201_CREATED)

    def get_sum_of_values_for_specific_column_filtered_by_datetime(
        self,
        db: Session,
        current_user: User,
        from_datetime: Optional[datetime],
        till_datetime: Optional[datetime],
    ) -> float:
        data = self.dal(self.model).read_many_offset_limit_filtered_by_datetime(
            db,
            from_datetime,
            till_datetime,
            skip=0,
            limit=99999,
            pharmacy_id=current_user.pharmacy.id,
        )
        sum_t: float = 0
        sum_d: float = 0
        sum_p: float = 0
        if not data:
            sum: dict = {
                "sum_of_total_amount": sum_t,
                "sum_of_due_amount": sum_d,
                "sum_of_paid_amount": sum_p,
            }
            return ServiceResult(sum, status_code=status.HTTP_204_NO_CONTENT)
        for item in data:
            sum_t += item.total_amount
            sum_d += item.due_amount
            sum_p += item.paid_amount
        sum: dict = {
            "sum_of_total_amount": sum_t,
            "sum_of_due_amount": sum_d,
            "sum_of_paid_amount": sum_p,
        }
        return ServiceResult(sum, status_code=status.HTTP_200_OK)


class InvoiceOrderLineService(
    BaseService[InvoiceOrderLineDAL, InvoiceOrderLineCreate, None]
):
    def create_along_with_invoice_order(
        self,
        db: Session,
        current_user: User,
        obj_in: List[InvoiceOrderLineCreate],
        invoice_order_id: int,
    ) -> bool:
        for every_invoice_order_line in obj_in:
            invoice_order_line = self.dal(self.model).create_without_commit_but_flush(
                db,
                obj_in=every_invoice_order_line,
                invoice_order_id=invoice_order_id,
            )
            if not invoice_order_line:
                return ServiceResult(
                    AppException.ServerError(
                        "Problem occured while adding invoice order lines"
                    )
                )

            """also decreasing stock quantity"""
            stock_service.decrease_stock_quantity_filtered_by_medicine_id_without_commit(  # noqa E501
                db,
                current_user,
                medicine_id=every_invoice_order_line.medicine_id,
                quantity=every_invoice_order_line.quantity,
            )
        return True


invoice_order_service = InvoiceOrderService(InvoiceOrderDAL, InvoiceOrder)


invoice_order_line_service = InvoiceOrderLineService(
    InvoiceOrderLineDAL, InvoiceOrderLine
)
