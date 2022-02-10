from typing import Optional
from pydantic import BaseModel


class MedicineCreate(BaseModel):
    brand_name: str
    generic_name: Optional[str]
    dosage_form: Optional[str]
    strength: Optional[str]
    unit_price: Optional[float]
    depo_price: Optional[float]
    manufacturer_id: int


class MedicineOut(MedicineCreate):
    id: int

    class Config:
        orm_mode = True


class MedicineUpdate(BaseModel):
    brand_name: Optional[str]
    generic_name: Optional[str]
    dosage_form: Optional[str]
    strength: Optional[str]
    unit_price: Optional[float]
    depo_price: Optional[float]
