from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_active_user
from db.config import get_db
from schemas import StockUpdate, StockOut
from models import User
from services import stock_service
from utils.service_result import handle_result

router = APIRouter()


@router.get("/", response_model=List[StockOut])
def get_all_stocks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
):
    stocks = stock_service.get_many(
        db, handle_result(current_user), skip=skip, limit=limit
    )
    return handle_result(stocks)


@router.get("/get_total_stock")
def get_total_medicine_quantity_in_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    value = stock_service.get_sum_of_in_stock_values_filtered_by_datetime(
        db, handle_result(current_user)
    )
    return {"value": handle_result(value)}


@router.put("/{stock_id}", response_model=StockOut)
def update_stock_by_id(
    stock_id: int,
    stock_update: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    stock = stock_service.update_by_id(
        db, handle_result(current_user), id=stock_id, obj_in=stock_update
    )
    return handle_result(stock)
