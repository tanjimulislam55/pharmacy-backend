from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import MedicineCreate, MedicineOut, MedicineUpdate
from src.models import User
from src.services import medicine_service
from src.utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=MedicineOut)
def create_medicine(
    medicine_in: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    medicine = medicine_service.create_along_with_stock(db, obj_in=medicine_in)
    return handle_result(medicine)


@router.get("/", response_model=List[MedicineOut])
def get_all_medicines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    medicines = medicine_service.get_many(db, skip=skip, limit=limit)
    return handle_result(medicines)


@router.get("/search/brand_name/", response_model=List[MedicineOut])
def get_medicines_by_brand_name_letters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    name_str: Optional[str] = None,
):
    medicines = medicine_service.get_many_by_brand_name_letters(
        db, name_str=name_str, skip=skip, limit=limit
    )
    return handle_result(medicines)


@router.get("/search/generic_name/", response_model=List[MedicineOut])
def get_medicines_by_generic_name_letters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    name_str: Optional[str] = None,
):
    medicines = medicine_service.get_many_by_generic_name_letters(
        db, name_str=name_str, skip=skip, limit=limit
    )
    return handle_result(medicines)


@router.get("/{medicine_id}", response_model=MedicineOut)
def get_medicine_by_id(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    medicine = medicine_service.get_one_by_id(db, id=medicine_id)
    return handle_result(medicine)


@router.put("/{medicine_id}", response_model=MedicineOut)
def update_medicine_by_id(
    medicine_id: int,
    medicine_update: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    medicine = medicine_service.update_by_id(db, id=medicine_id, obj_in=medicine_update)
    return handle_result(medicine)
