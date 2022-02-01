from .base import BaseService
from src.dals import ManufacturerDAL
from src.models import Manufacturer
from src.schemas import ManufacturerCreate, ManufacturerUpdate


class ManufacturerService(
    BaseService[ManufacturerDAL, ManufacturerCreate, ManufacturerUpdate]
):
    pass


manufacturer_service = ManufacturerService(ManufacturerDAL, Manufacturer)
