from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StockCreate(BaseModel):
    in_stock: Optional[int] = 0
    critical_stock: Optional[int] = 0
    last_date_of_purchase: Optional[datetime]
    last_purchased_quantity: Optional[int] = 0
    medicine_id: int


class StockOut(StockCreate):
    id: int

    class Config:
        orm_mode = True


class StockUpdate(BaseModel):
    in_stock: Optional[int]
    critical_stock: Optional[int]
    last_date_of_purchase: Optional[datetime]
    last_purchased_quantity: Optional[int]
