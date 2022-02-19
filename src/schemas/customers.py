from datetime import date
from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from typing import Optional

from utils.enums import GenderEnum, BloodGroupEnum


class CustomerCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr]
    phone: constr(
        min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}"  # noqa: F722
    )
    gender: GenderEnum
    bloodgroup: Optional[BloodGroupEnum]
    birthdate: Optional[date]


class CustomerUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[
        constr(min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}")  # noqa: F722
    ]
    gender: Optional[GenderEnum]
    bloodgroup: Optional[BloodGroupEnum]
    birthdate: Optional[date]


class CustomerOut(CustomerCreate):
    id: int

    class Config:
        orm_mode = True


class UserInDB(CustomerCreate):
    pass
