from sqlalchemy.orm import Session

from . import models, schemas
from ..helpers import get_datetime_now
from ..services import CategoryService


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    print(user)
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=fake_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    category_service = CategoryService(db, task)
    db_task = models.Task(**task.dict(exclude={"categories"}), owner_id=user_id)
    categories = category_service.get_categories_by_ids(task.categories)
    db_task.categories.extend(categories)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Category)
            .filter(models.Category.deleted_at == None)
            .offset(skip).limit(limit).all())


def create_task_category(db: Session, category: schemas.CategoryCreate, task_id: int):
    db_category = models.Category(**category.dict(), task_id=task_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id,
                                            models.Category.deleted_at == None).first()


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
