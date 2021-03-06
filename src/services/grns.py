from sqlalchemy.orm import Session
from fastapi import status
from typing import List, Optional
from datetime import datetime

from .base import BaseService
from .stocks import stock_service
from .medicines import medicine_service
from .purchases import purchase_order_service
from .manufacturers import trade_history_service
from dals import GRNDAL
from models import GRN, Medicine, User
from schemas import GRNCreate, GRNUpdate, StockUpdate
from utils.service_result import ServiceResult, handle_result
from utils.app_exceptions import AppException


class GRNService(BaseService[GRNDAL, GRNCreate, GRNUpdate]):
    def create(self, db: Session, current_user: User, obj_in: List[GRNCreate]):
        manu_id_dict_by_med_id: dict = {}
        for every_grn_obj in obj_in:
            """check if stock exists by medicine id. if not then create stock"""
            existing_stock = stock_service.get_one_by_pharmacy_id(
                db, current_user, medicine_id=every_grn_obj.medicine_id
            )
            if not existing_stock:
                stock_service.create(
                    db,
                    current_user,
                    medicine_id=every_grn_obj.medicine_id,
                )
            "" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
            medicine = medicine_service.get_one_by_id(db, id=every_grn_obj.medicine_id)
            medicine_object: Medicine = handle_result(medicine)
            manu_id_dict_by_med_id.update(
                {medicine_object.id: medicine_object.manufacturer_id}
            )
            if not medicine:
                return ServiceResult(
                    AppException.NotFound(
                        f"No medicine found with id: {every_grn_obj.medicine_id}"
                    )
                )
            if not purchase_order_service.get_one_by_id(
                db, id=every_grn_obj.purchase_id, current_user=current_user
            ):
                return ServiceResult(
                    AppException.NotFound(
                        f"No purchase order found with id: {every_grn_obj.purchase_id}"  # noqa E501
                    )
                )
        """to store all grn objects"""
        grns: List[GRN] = []
        """to calculate total grn costs"""
        total_cost_from_grns: float = 0
        for every_grn_obj in obj_in:
            grn = self.dal(self.model).create_without_commit_but_flush(
                db, obj_in=every_grn_obj, pharmacy_id=current_user.pharmacy.id
            )
            if not grn:
                return ServiceResult(AppException.ServerError("Something went wrong"))
            grns.append(grn)
            """also increasing stock quantity"""
            stock_service.increase_stock_quantity_filtered_by_medicine_id_without_commit(
                db,
                current_user,
                medicine_id=every_grn_obj.medicine_id,
                quantity=every_grn_obj.quantity,
            )
            stock_service.update_filtered_by_medicine_id(
                db,
                current_user,
                medicine_id=every_grn_obj.medicine_id,
                obj_in=StockUpdate(
                    last_date_of_purchase=datetime.now(),
                    last_purchased_quantity=every_grn_obj.quantity,
                ),
            )
            total_cost_from_grns += every_grn_obj.cost
        """also initiating trade histories"""
        trade_history_service.create_along_with_grn(
            db,
            current_user,
            manufacturer_id=manu_id_dict_by_med_id[every_grn_obj.medicine_id],
            amount=total_cost_from_grns,
        )
        return [ServiceResult(grn, status_code=status.HTTP_201_CREATED) for grn in grns]

    def get_many_filtered_by_expiry_date(
        self,
        db: Session,
        current_user: User,
        from_datetime: Optional[datetime],
        till_datetime: Optional[datetime],
        skip: int = 0,
        limit: int = 10,
    ):
        data = self.dal(self.model).read_many_offset_limit_filtered_by_expiry_date(
            db,
            from_datetime,
            till_datetime,
            skip=skip,
            limit=limit,
            pharmacy_id=current_user.pharmacy.id,
        )
        if not data:
            return ServiceResult(
                AppException.NotFound(f"No {self.model.__name__.lower()}s found")
            )
        return ServiceResult(data, status_code=status.HTTP_200_OK)

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
        sum_c: float = 0
        sum_q: float = 0
        if not data:
            sum: dict = {"sum_of_cost": sum_c, "sum_of_quantity": sum_q}
            return ServiceResult(sum, status_code=status.HTTP_204_NO_CONTENT)
        for item in data:
            sum_c += item.cost
            sum_q += item.quantity
        sum: dict = {"sum_of_cost": sum_c, "sum_of_quantity": sum_q}
        return ServiceResult(sum, status_code=status.HTTP_200_OK)

    def get_sum_of_values_for_specific_column_filtered_by_expiry_date(
        self,
        db: Session,
        current_user: User,
        from_datetime: Optional[datetime],
        till_datetime: Optional[datetime],
    ) -> float:
        data = self.dal(self.model).read_many_offset_limit_filtered_by_expiry_date(
            db,
            from_datetime,
            till_datetime,
            skip=0,
            limit=99999,
            pharmacy_id=current_user.pharmacy.id,
        )
        sum_c: float = 0
        sum_q: float = 0
        if not data:
            sum: dict = {"sum_of_cost": sum_c, "sum_of_quantity": sum_q}
            return ServiceResult(sum, status_code=status.HTTP_204_NO_CONTENT)
        for item in data:
            sum_c += item.cost
            sum_q += item.quantity
        sum: dict = {"sum_of_cost": sum_c, "sum_of_quantity": sum_q}
        return ServiceResult(sum, status_code=status.HTTP_200_OK)


grn_service = GRNService(GRNDAL, GRN)
