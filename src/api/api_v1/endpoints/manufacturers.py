from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import ManufacturerCreate, ManufacturerOut
from src.models import User
from src.services import manufacturer_service
from src.utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=ManufacturerOut)
def create_manufacturer(
    manufacturer_in: ManufacturerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    manufacturer = manufacturer_service.create_along_with_trade(
        db, obj_in=manufacturer_in
    )
    return handle_result(manufacturer)


@router.get("/", response_model=List[ManufacturerOut])
def get_all_manufacturers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    manufacturers = manufacturer_service.get_many(db, skip=skip, limit=limit)
    return handle_result(manufacturers)


@router.get("/{manufacturer_id}", response_model=ManufacturerOut)
def get_manufacturer_by_id(
    manufacturer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    manufacturer = manufacturer_service.get_one_by_id(db, id=manufacturer_id)
    return handle_result(manufacturer)
