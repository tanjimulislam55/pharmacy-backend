from schemas import RoleCreate, RoleUpdate
from models import Role
from .base import BaseService
from dals import RoleDAL


class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    pass


role_service = RoleService(RoleDAL, Role)
