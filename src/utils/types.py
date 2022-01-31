from typing import TypeVar
from pydantic import BaseModel
from src.db.config import Base
from src.dals.base import BaseDAL


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelDAL = TypeVar("ModelDAL", bound=BaseDAL)
