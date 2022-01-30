from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(RoleCreate):
    pass


class Role(RoleCreate):
    id: int

    class Config:
        orm_mode = True
