from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import UserCreate, UserOut
from src.services.users import user_service
from src.utils.service_result import handle_result
from src.models import User

router = APIRouter()


@router.post("/new", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create(db, obj_in=user_in)
    return handle_result(user)


@router.get("/", response_model=List[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    users = user_service.get_many(db, skip=skip, limit=limit)
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
