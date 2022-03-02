from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_active_user
from db.config import get_db
from schemas import UserCreate, UserOut, PharmacyCreate
from models import User
from services import user_service
from utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=UserOut)
def create_user(
    user_in: UserCreate,
    pharmacy_in: Optional[PharmacyCreate] = None,
    db: Session = Depends(get_db),
):
    user = user_service.create(db, obj_in=user_in, pharmacy_in=pharmacy_in)
    return handle_result(user)


@router.get("/", response_model=List[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    users = user_service.get_many(
        db, handle_result(current_user), skip=skip, limit=limit
    )
    return handle_result(users)


@router.get("/me", response_model=UserOut)
def get_user_me(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return handle_result(current_user)


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user = user_service.get_one_by_id(db, id=user_id)
    return handle_result(user)


@router.put("/active/{user_id}", response_model=UserOut)
def active_a_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user = user_service.activate_user(db, handle_result(current_user), id=user_id)
    return handle_result(user)


@router.put("/update/{user_id}/role/{role_id}", response_model=UserOut)
def update_user_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user = user_service.update_user_role(
        db, handle_result(current_user), id=user_id, role_id=role_id
    )
    return handle_result(user)
