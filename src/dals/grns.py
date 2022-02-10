from .base import BaseDAL
from src.models import GRN
from src.schemas import GRNCreate, GRNUpdate


class GRNDAL(BaseDAL[GRN, GRNCreate, GRNUpdate]):
    pass
