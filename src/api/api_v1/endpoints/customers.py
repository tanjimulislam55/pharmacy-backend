from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_active_user, get_db
from src.schemas import CustomerCreate, CustomerUpdate, CustomerOut
from src.models import User
from src.services import customer_service
from src.utils.service_result import handle_result

router = APIRouter()


@router.post("/new", response_model=CustomerOut)
def create_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    customer = customer_service.create(db, obj_in=customer_in)
    return handle_result(customer)


@router.get("/", response_model=List[CustomerOut])
def get_all_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    customers = customer_service.get_many(db, skip=skip, limit=limit)
    return handle_result(customers)


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer_by_id(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    customer = customer_service.get_one_by_id(db, id=customer_id)
    return handle_result(customer)


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer_by_id(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    customer = customer_service.update_by_id(db, id=customer_id, obj_in=customer_update)
    return handle_result(customer)
