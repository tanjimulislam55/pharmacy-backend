from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from typing import Optional

from .pharmacies import PharmacyOut


class UserBase(BaseModel):
    full_name: str
    email: Optional[EmailStr]
    phone: constr(
        min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}"  # noqa: F722
    )


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[
        constr(min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}")  # noqa: F722
    ]
    password: Optional[str]
    is_active: Optional[bool]


class UserOut(UserBase):
    id: int
    is_active: bool
    pharmacy: Optional[PharmacyOut] = None

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True


class UserInDB(UserBase):
    password: str
    is_active: bool = False
