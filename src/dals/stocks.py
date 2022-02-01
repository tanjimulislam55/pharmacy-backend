from .base import BaseDAL
from src.models import Stock
from src.schemas import StockCreate, StockUpdate


class StockDAL(BaseDAL[Stock, StockCreate, StockUpdate]):
    pass
