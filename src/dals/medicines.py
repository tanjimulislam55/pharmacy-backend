from .base import BaseDAL
from src.models import Medicine
from src.schemas import MedicineCreate, MedicineUpdate


class MedicineDAL(BaseDAL[Medicine, MedicineCreate, MedicineUpdate]):
    pass
