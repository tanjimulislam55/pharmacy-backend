from pydantic import BaseModel
from typing import List, Optional


class ManufacturerCreate(BaseModel):
    name: str
    total_brands: Optional[int]
    total_generics: Optional[int]
    headquarter: Optional[str]
    contact_list: Optional[List[str]]
    established_in: Optional[str]
    market_share: Optional[str]
    growth: Optional[str]


class ManufacturerOut(ManufacturerCreate):
    id: int

    class Config:
        orm_mode = True
