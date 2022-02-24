from sqlalchemy.orm import Session
from typing import Optional, List

from .base import BaseDAL
from models import Medicine, Stock
from schemas import MedicineCreate, MedicineUpdate


class MedicineDAL(BaseDAL[Medicine, MedicineCreate, MedicineUpdate]):
    def create_with_commit(self, db: Session, obj_in: MedicineCreate) -> Medicine:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_many_offset_limit(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Medicine]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def read_many_filtered_by_brand_name_letters(
        self, db: Session, name_str: Optional[str], skip: int = 0, limit: int = 10
    ) -> Optional[List[Medicine]]:
        return (
            db.query(self.model)
            .filter(self.model.brand_name.like(f"{name_str}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def read_one_filtered_by_id(self, db: Session, id: int) -> Optional[Medicine]:
        return db.query(self.model).filter(self.model.id == id).first()

    def update_one_filtered_by_id(
        self, db: Session, id: int, obj_in: MedicineUpdate
    ) -> Medicine:
        db.query(self.model).filter(self.model.id == id).update(
            obj_in.dict(exclude_unset=True), synchronize_session=False
        )
        db.commit()
        return self.read_one_filtered_by_id(db, id)

    def read_many_filtered_by_generic_name_letters(
        self, db: Session, name_str: Optional[str], skip: int = 0, limit: int = 10
    ) -> Optional[List[Medicine]]:
        return (
            db.query(self.model)
            .filter(self.model.generic_name.like(f"{name_str}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def read_many_filtered_by_manufacturer_id(
        self, db: Session, manufacturer_id: int, skip: int = 0, limit: int = 10
    ) -> Optional[List[Medicine]]:
        return (
            db.query(self.model)
            .filter(self.model.manufacturer_id == manufacturer_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def read_many_filtered_by_manufacturer_id_and_brand_name(
        self,
        db: Session,
        manufacturer_id: int,
        name_str: Optional[str],
        skip: int = 0,
        limit: int = 10,
    ) -> Optional[List[Medicine]]:
        return (
            db.query(self.model)
            .filter(self.model.manufacturer_id == manufacturer_id)
            .filter(self.model.brand_name.like(f"{name_str}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def read_many_join_with_stock(
        self, db: Session, pharmacy_id: int
    ) -> List[Optional[Medicine]]:
        return (
            db.query(
                Medicine.id, Medicine.brand_name, Medicine.unit_price, Stock.in_stock
            )
            .filter(Stock.pharmacy_id == pharmacy_id)
            .join(
                Stock,
                Medicine.id == Stock.medicine_id,
            )
            .all()
        )
