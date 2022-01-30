from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from typing import Optional

from src.utils.enums import GenderEnum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    phone: constr(
        min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}"  # noqa: F722
    )
    gender: GenderEnum


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[
        constr(min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}")  # noqa: F722
    ]
    gender: Optional[GenderEnum]
    password: Optional[str]
    is_active: Optional[bool]


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str
    is_active: bool = False
    is_superuser: bool = False
