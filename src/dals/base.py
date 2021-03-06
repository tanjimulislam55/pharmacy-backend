from typing import Any, Generic, List, Optional, Type, Union, TypeVar
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from db.config import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAL(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def just_commit_and_return_db_obj(
        self, db: Session, db_obj: ModelType
    ) -> ModelType:
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_commit(
        self, db: Session, pharmacy_id: int, obj_in: CreateSchemaType
    ) -> ModelType:
        db_obj = self.model(**obj_in.dict(), pharmacy_id=pharmacy_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_without_commit_but_flush(
        self, db: Session, pharmacy_id: int, obj_in: CreateSchemaType
    ) -> ModelType:
        db_obj = self.model(**obj_in.dict(), pharmacy_id=pharmacy_id)
        db.add(db_obj)
        db.flush()
        return db_obj

    def read_one_filtered_by_id(
        self, db: Session, id: int, pharmacy_id: int
    ) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.id == id, self.model.pharmacy_id == pharmacy_id)
            .first()
        )

    def read_many_offset_limit(
        self, db: Session, pharmacy_id: int, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.pharmacy_id == pharmacy_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def read_many_offset_limit_filtered_by_datetime(
        self,
        db: Session,
        from_datetime: Optional[datetime],
        till_datetime: Optional[datetime],
        pharmacy_id: int,
        skip: int = 0,
        limit: int = 10,
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(
                self.model.pharmacy_id == pharmacy_id,
                self.model.created_at.between(from_datetime, till_datetime),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def read_all(self, db: Session, pharmacy_id: int) -> List[ModelType]:
        return db.query(self.model).filter(self.model.pharmacy_id == pharmacy_id).all()

    def update_one_filtered_by_id(
        self, db: Session, id: int, pharmacy_id: int, obj_in: UpdateSchemaType
    ) -> ModelType:
        db.query(self.model).filter(
            self.model.id == id, self.model.pharmacy_id == pharmacy_id
        ).update(obj_in.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return self.read_one_filtered_by_id(db, id)

    def delete_one_filtered_by_id(
        self, db: Session, id: int, pharmacy_id: int
    ) -> Optional[Union[ModelType, Any]]:
        if (
            db.query(self.model)
            .filter(self.model.id == id, self.model.pharmacy_id == pharmacy_id)
            .delete(synchronize_session=False)
        ):
            db.commit()
            return True
        else:
            return False
