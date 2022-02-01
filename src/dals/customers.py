from typing import Optional
from sqlalchemy.orm import Session

from .base import BaseDAL
from src.models import Customer
from src.schemas import CustomerCreate, CustomerUpdate


class CustomerDAL(BaseDAL[Customer, CustomerCreate, CustomerUpdate]):
    def read_one_filtered_by_phone(self, db: Session, phone: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.phone == phone).first()


customer_dal = CustomerDAL(Customer)
