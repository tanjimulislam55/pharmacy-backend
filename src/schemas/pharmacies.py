from pydantic import BaseModel
from typing import Optional


class PharmacyCreate(BaseModel):
    name: str
    trade_license: str
    area: str
    sub_district: str
    district: str


class PharmacyInDB(PharmacyCreate):
    user_id: int


class PharmacyUpdate(PharmacyCreate):
    name: Optional[str]
    area: Optional[str]
    sub_district: Optional[str]
    district: Optional[str]


class PharmacyOut(PharmacyCreate):
    id: int

    class Config:
        orm_mode = True
