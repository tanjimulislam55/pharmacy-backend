from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import MedicineCreate, MedicineOut, MedicineUpdate, MedicineJoinStock
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


@router.get("/join/stock", response_model=List[MedicineJoinStock])
def get_all_medicines_joined_with_stocks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    medicines = medicine_service.get_many_join_with_stock(db)
    return handle_result(medicines)


@router.get("/get_medicine_costs_of_stock")
def get_medicine_costs_of_stock(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    value = medicine_service.calculate_total_stock_costs(db)
    return {"value": handle_result(value)}


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


@router.get("/search/brand_name/{manufacturer_id}", response_model=List[MedicineOut])
def get_medicines_by_brand_name_letters_and_manufacturer_id(
    manufacturer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    name_str: Optional[str] = None,
):
    medicines = medicine_service.get_many_by_manufacturer_id_and_brand_name_letters(
        db, manufacturer_id=manufacturer_id, name_str=name_str, skip=skip, limit=limit
    )
    return handle_result(medicines)


@router.get("/search/{manufacturer_id}", response_model=List[MedicineOut])
def get_medicines_by_manufacturer_id(
    manufacturer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    medicines = medicine_service.get_many_by_manufacturer_id(
        db, manufacturer_id=manufacturer_id, skip=skip, limit=limit
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
