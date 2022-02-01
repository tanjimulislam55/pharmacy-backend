from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StockCreate(BaseModel):
    in_stock: Optional[int]
    last_transacted_date: Optional[datetime]
    last_transacted_quantity: Optional[int]
    medicine_id: int


class StockOut(StockCreate):
    id: int

    class Config:
        orm_mode = True


class StockUpdate(BaseModel):
    in_stock: Optional[int]
    last_transacted_date: Optional[datetime]
    last_transacted_quantity: Optional[int]
