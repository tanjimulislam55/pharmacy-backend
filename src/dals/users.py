from typing import Optional, List
from sqlalchemy.orm import Session

from .base import BaseDAL
from models import User
from schemas import UserCreate, UserUpdate


class UserDAL(BaseDAL[User, UserCreate, UserUpdate]):
    def create_with_commit(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_without_commit_but_flush(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        return db_obj

    def read_many_offset_limit(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return db.query(self.model).offset(skip).limit(limit).all()

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
