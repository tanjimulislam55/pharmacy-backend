from .base import BaseDAL
from src.models import Manufacturer
from src.schemas import ManufacturerCreate, ManufacturerUpdate


class ManufacturerDAL(BaseDAL[Manufacturer, ManufacturerCreate, ManufacturerUpdate]):
    pass
