from sqlalchemy.orm import Session
from typing import Optional

from .base import BaseDAL
from models import Pharmacy
from schemas import PharmacyCreate, PharmacyUpdate


class PharmacyDAL(BaseDAL[Pharmacy, PharmacyCreate, PharmacyUpdate]):
    def create_with_commit(self, db: Session, obj_in: PharmacyCreate) -> Pharmacy:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_one_filtered_by_trade_license(
        self, db: Session, trade_license: str
    ) -> Optional[Pharmacy]:
        return (
            db.query(self.model)
            .filter(self.model.trade_license == trade_license)
            .first()
        )
