from typing import Optional
from sqlalchemy.orm import Session

from .base import BaseDAL
from models import Role
from schemas import RoleCreate, RoleUpdate


class RoleDAL(BaseDAL[Role, RoleCreate, RoleUpdate]):
    def create_with_commit(self, db: Session, obj_in: RoleCreate) -> Role:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_one_filtered_by_id(self, db: Session, id: int) -> Optional[Role]:
        return db.query(self.model).filter(self.model.id == id).first()
