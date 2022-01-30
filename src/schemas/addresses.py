from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    flat: Optional[str]
    house: Optional[str]
    road: Optional[str]
    block: Optional[str]
    area: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]


class AddressCreate(AddressBase):
    user_id: Optional[int]
    customer_id: Optional[int]


class AddressUpdate(AddressBase):
    pass


class AddressOut(AddressBase):
    id: int

    class Config:
        orm_mode = True
