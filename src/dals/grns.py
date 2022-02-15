from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List

from .base import BaseDAL
from src.models import GRN
from src.schemas import GRNCreate, GRNUpdate


class GRNDAL(BaseDAL[GRN, GRNCreate, GRNUpdate]):
    def read_many_offset_limit_filtered_by_expiry_date(
        self,
        db: Session,
        from_datetime: Optional[datetime],
        till_datetime: Optional[datetime],
        skip: int = 0,
        limit: int = 10,
    ) -> List[GRN]:
        return (
            db.query(self.model)
            .filter(self.model.expiry_date.between(from_datetime, till_datetime))
            .offset(skip)
            .limit(limit)
            .all()
        )
