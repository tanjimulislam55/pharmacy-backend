from sqlalchemy.orm import Session

from .base import BaseService
from dals import PharmacyDAL
from models import Pharmacy
from schemas import PharmacyCreate, PharmacyUpdate, PharmacyInDB
from utils.service_result import ServiceResult
from utils.app_exceptions import AppException


class PharmacyService(BaseService[PharmacyDAL, PharmacyCreate, PharmacyUpdate]):
    def create_along_with_user(self, db: Session, obj_in: PharmacyCreate, user_id: int):
        db_obj = obj_in.dict()
        db_obj["user_id"] = user_id
        pharmacy = self.dal(self.model).create_with_commit(
            db, obj_in=PharmacyInDB(**db_obj)
        )
        if not pharmacy:
            return ServiceResult(
                AppException.ServerError("Problem occured while adding medicine")
            )
        return pharmacy

    def get_one_by_trade_license(self, db: Session, trade_license: str) -> Pharmacy:
        return self.dal(self.model).read_one_filtered_by_trade_license(
            db, trade_license
        )


pharmacy_service = PharmacyService(PharmacyDAL, Pharmacy)
