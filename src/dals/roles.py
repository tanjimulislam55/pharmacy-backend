from typing import Optional
from sqlalchemy.orm import Session

from .base import BaseDAL
from models import Role
from schemas import RoleCreate, RoleUpdate


class RoleDAL(BaseDAL[Role, RoleCreate, RoleUpdate]):
    def read_one_filtered_by_id(self, db: Session, id: int) -> Optional[Role]:
        return db.query(self.model).filter(self.model.id == id).first()
