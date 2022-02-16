from typing import List, Optional
from datetime import datetime
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
    value = grn_service.get_sum_of_values_for_specific_column_filtered_by_datetime(  # noqa E501
        db,
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
    value = grn_service.get_sum_of_values_for_specific_column_filtered_by_expiry_date(  # noqa E501
        db,
        from_datetime=from_datetime,
        till_datetime=till_datetime,
    )
    return handle_result(value)
