from datetime import date
from typing import Optional
from pydantic import BaseModel


class GRNCreate(BaseModel):
    quantity: int
    depo_price: float
    vat: Optional[int] = 0
    discount: Optional[int] = 0
    cost: float
    expiry_date: Optional[date]
    medicine_id: int
    purchase_id: int
    manufacturer_id: int


class GRNOut(GRNCreate):
    id: int

    class Config:
        orm_mode = True


class GRNUpdate(BaseModel):
    quantity: int
    depo_price: float
    vat: Optional[int] = 0
    discount: Optional[int] = 0
    cost: float
    expiry_date: Optional[date]
