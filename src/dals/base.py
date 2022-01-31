from typing import Any, Generic, List, Optional, Type, Union
from sqlalchemy.orm import Session

from src.utils.types import CreateSchemaType, ModelType, UpdateSchemaType


class BaseDAL(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create_with_commit(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_one_filtered_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def read_many_offset_limit(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def read_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def update_one_filtered_by_id(
        self, db: Session, id: int, obj_in: UpdateSchemaType
    ) -> ModelType:
        db.query(self.model).filter(self.model.id == id).update(
            obj_in.dict(exclude_unset=True), synchronize_session=False
        )
        return self.read_one_by_id(db, id)

    def delete_one_filtered_by_id(
        self, db: Session, id: int
    ) -> Optional[Union[ModelType, Any]]:
        return (
            db.query(self.model)
            .filter(self.model.id == id)
            .delete(synchronize_session=False)
        )
