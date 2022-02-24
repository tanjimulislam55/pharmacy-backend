from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TradeCreate(BaseModel):
    closing_balance: Optional[float] = 0
    outstanding_amount: Optional[float] = 0
    overdue_amount: Optional[float] = 0


class TradeOut(TradeCreate):
    id: int
    manufacturer_id: int

    class Config:
        orm_mode = True


class TradeUpdate(BaseModel):
    closing_balance: Optional[float]
    outstanding_amount: Optional[float]
    overdue_amount: Optional[float]


class TradeHistoryCreate(BaseModel):
    purchased_amount: Optional[float] = 0


class TradeHistoryOut(TradeHistoryCreate):
    id: int
    manufacturer_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TradeHistoryUpdate(BaseModel):
    purchased_amount: Optional[float]


class ManufacturerCreate(BaseModel):
    name: str


class ManufacturerOut(ManufacturerCreate):
    id: int

    class Config:
        orm_mode = True


class ManufacturerUpdate(BaseModel):
    name: Optional[str]
    total_brands: Optional[int]
    total_generics: Optional[int]
    headquarter: Optional[str]
    contact_list: Optional[List[str]]
    established_in: Optional[str]
    market_share: Optional[str]
    growth: Optional[str]
