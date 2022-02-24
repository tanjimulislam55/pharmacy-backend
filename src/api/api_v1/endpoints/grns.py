from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_active_user
from db.config import get_db
from schemas import GRNCreate, GRNOut
from models import User
from services import grn_service
from utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=List[GRNOut])
def create_grns(
    grn_in: List[GRNCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    grns = grn_service.create(db, handle_result(current_user), obj_in=grn_in)
    return [handle_result(grn) for grn in grns]


@router.get("/", response_model=List[GRNOut])
def get_all_grns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    grns = grn_service.get_many(db, handle_result(current_user), skip=skip, limit=limit)
    return handle_result(grns)


@router.get("/filtered_by_expiry_date/", response_model=List[GRNOut])
def get_all_grns_filtered_by_expiry_date(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    from_datetime: Optional[datetime] = datetime.strptime(
        "2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
    ),
    till_datetime: Optional[datetime] = str(datetime.now()),
):
    grns = grn_service.get_many_filtered_by_expiry_date(
        db,
        handle_result(current_user),
        from_datetime=from_datetime,
        till_datetime=till_datetime,
        skip=skip,
        limit=limit,
    )
    return handle_result(grns)


@router.get("/get_sum_filtered_by_datetime/")
def get_sum_filtered_by_datetime(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    from_datetime: Optional[datetime] = datetime.strptime(
        "2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
    ),
    till_datetime: Optional[datetime] = str(datetime.now()),
):
    value = grn_service.get_sum_of_values_for_specific_column_filtered_by_datetime(
        db,
        handle_result(current_user),
        from_datetime=from_datetime,
        till_datetime=till_datetime,
    )
    return handle_result(value)


@router.get("/get_sum_filtered_by_expiry_date/")
def get_sum_filtered_by_expiry_date(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    from_datetime: Optional[datetime] = datetime.strptime(
        "2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
    ),
    till_datetime: Optional[datetime] = str(datetime.now()),
):
    value = grn_service.get_sum_of_values_for_specific_column_filtered_by_expiry_date(
        db,
        handle_result(current_user),
        from_datetime=from_datetime,
        till_datetime=till_datetime,
    )
    return handle_result(value)
