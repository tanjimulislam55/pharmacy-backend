from typing import Optional
from sqlalchemy.orm import Session

from .base import BaseDAL
from models import User
from schemas import UserCreate, UserUpdate


class UserDAL(BaseDAL[User, UserCreate, UserUpdate]):
    def read_one_filtered_by_id(self, db: Session, id: int) -> Optional[User]:
        return db.query(self.model).filter(self.model.id == id).first()

    def read_one_filtered_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def read_one_filtered_by_phone(self, db: Session, phone: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.phone == phone).first()

    def update_one_filtered_by_id_to_activate_user(self, db: Session, id: int) -> User:
        db.query(self.model).filter(self.model.id == id).update(
            {self.model.is_active: True}, synchronize_session=False
        )
        db.commit()
        return self.read_one_filtered_by_id(db, id)
