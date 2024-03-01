from sqlalchemy.orm import Session

from src.app.helpers import get_datetime_now, compare_max_date
from src.app.services import CategoryService
from src.app.sql_app import models, schemas
from src.app.sql_app.models import Task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Task)
            .filter(models.Task.deleted_at == None)
            .offset(skip).limit(limit).all())


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.deleted_at == None
    ).first()


def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task: Task | None = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None

    db_task.title = task.title
    db_task.description = task.description
    db_task.minutes_expected = task.minutes_expected
    db_task.minutes_completed = task.minutes_completed
    if task.minutes_total:
        db_task.minutes_total = task.minutes_total
    db_task.priority = task.priority
    db_task.defeated = task.defeated
    db_task.type = task.type
    db_task.repeat = task.repeat
    db_task.expiration_date = task.expiration_date
    print(task.expiration_date, "expiration_date - request")
    print(db_task.expiration_date, "expiration_date - db")
    if task.repeated_date:
        db_task.repeated_date = task.repeated_date
    if task.repeated_days:
        db_task.repeated_days = task.repeated_days
    # validate date expiration
    if compare_max_date(task.expiration_date):
        db_task.defeated = 1

    # if type = 2, then is defeated is 0
    if task.type == 2:
        db_task.defeated = 0
    db_task.alert_id = task.alert_id
    db_task.updated_at = get_datetime_now()
    category_service = CategoryService(db, task)
    categories = category_service.get_categories_by_ids(task.categories)
    db_task.categories.clear()
    db_task.categories.extend(categories)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.deleted_at == None).first()
    if db_task is None:
        return None

    db_task.status = 2
    db_task.deleted_at = get_datetime_now()
    print(db_task.deleted_at)
    db.commit()
    db.refresh(db_task)
    return {
        "status": "success",
        "message": "Task deleted successfully"
    }


def create_history_task(db: Session, task: schemas.TaskCreate, history_id: int):
    category_service = CategoryService(db, task)
    db_task = models.Task(**task.model_dump(exclude={"categories", "created_at"}), history_id=history_id)
    categories = category_service.get_categories_by_ids(task.categories)
    db_task.categories.extend(categories)
    db_task.created_at = get_datetime_now()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def create_task_category(db: Session, category: schemas.CategoryCreate, task_id: int):
    db_category = models.Category(**category.dict(), task_id=task_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
