from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import GRNCreate, GRNOut
from src.models import User
from src.services import grn_service
from src.utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=List[GRNOut])
def create_grns(
    grn_in: List[GRNCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    grns = grn_service.create(db, obj_in=grn_in)
    return [handle_result(grn) for grn in grns]


@router.get("/", response_model=List[GRNOut])
def get_all_grns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    grns = grn_service.get_many(db, skip=skip, limit=limit)
    return handle_result(grns)
