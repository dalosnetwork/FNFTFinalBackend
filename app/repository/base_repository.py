from sqlalchemy.orm import Session
from app.repository.session import get_db
from fastapi import Depends

class BaseRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_by_field(self, field: str, value):
        return self.db.query(self.model).filter(getattr(self.model, field) == value).first()

    def create(self, **kwargs):
        db_obj = self.model(**kwargs)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int):
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    def list_all(self):
        return self.db.query(self.model).all()
