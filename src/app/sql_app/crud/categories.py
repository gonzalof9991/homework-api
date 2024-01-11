from sqlalchemy.orm import Session

from src.app.helpers import get_datetime_now
from src.app.sql_app import models, schemas


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump(exclude={"created_at"}))
    db_category.created_at = get_datetime_now()
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id,
                                            models.Category.deleted_at == None).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Category)
            .filter(models.Category.deleted_at == None)
            .offset(skip).limit(limit).all())


def update_category(db: Session, category_id: int, category: schemas.Category):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    db_category.name = category.name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    db_category.status = "deleted"
    db_category.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_category)
    return {
        "status": "success",
        "message": "Category deleted successfully"
    }
