from typing import TypeVar
from pydantic import BaseModel
from db.config import Base
from dals.base import BaseDAL


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ModelDAL = TypeVar("ModelDAL", bound=BaseDAL)


# there is problem with - partially initialized module - most likely due to circular import # noqa E501
