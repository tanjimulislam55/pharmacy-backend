from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import Role, RoleCreate, RoleUpdate
from api.deps import get_current_active_user
from db.config import get_db
from models import User
from services import role_service
from utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=Role)
def create_role(
    role_in: RoleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    role = role_service.create(db, obj_in=role_in)
    return handle_result(role)


@router.put("/{role_id}", response_model=Role)
def update_role_by_id(
    role_id: int,
    update_role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    role = role_service.update_by_id(db, id=role_id, obj_in=update_role)
    return handle_result(role)
