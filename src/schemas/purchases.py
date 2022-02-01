from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class PurchaseOrderLineCreate(BaseModel):
    quantity: int
    buying_price: float
    selling_price: float
    cost: float
    expiry_date: Optional[date]
    medicine_id: int


class PurchaseOrderLineOut(PurchaseOrderLineCreate):
    id: int
    purchase_id: int

    class Config:
        orm_mode = True


class PurchaseOrderCreate(BaseModel):
    total_amount: float
    paid_amount: float
    due_amount: float
    note: Optional[str]
    user_id: int


class PurchaseOrderOut(PurchaseOrderCreate):
    id: int
    purchase_lines: Optional[List[PurchaseOrderLineOut]] = None

    class Config:
        orm_mode = True


class PurchaseOrderUpdate(BaseModel):
    total_amount: Optional[float]
    paid_amount: Optional[float]
    due_amount: Optional[float]
    note: Optional[str]
