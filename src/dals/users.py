from typing import Optional
from sqlalchemy.orm import Session

from .base import BaseDAL
from src.models import User
from src.schemas import UserCreate, UserUpdate


class UserDAL(BaseDAL[User, UserCreate, UserUpdate]):
    def read_one_filtered_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def read_one_filtered_by_phone(self, db: Session, phone: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.phone == phone).first()
