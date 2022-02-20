from .base import BaseDAL
from models import Role
from schemas import RoleCreate, RoleUpdate


class RoleDAL(BaseDAL[Role, RoleCreate, RoleUpdate]):
    pass
