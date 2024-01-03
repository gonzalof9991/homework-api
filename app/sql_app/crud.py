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
    return (db.query(models.Task)
            .filter(models.Task.deleted_at == None)
            .offset(skip).limit(limit).all())


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.deleted_at == None
    ).first()


def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.title = task.title
    db_task.description = task.description
    db_task.minutes_expected = task.minutes_expected
    db_task.minutes_completed = task.minutes_completed
    db_task.priority = task.priority
    db_task.defeated = task.defeated
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
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.status = "deleted"
    db_task.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_task)
    return {
        "status": "success",
        "message": "Task deleted successfully"
    }


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


# ALERTS

def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Alert)
            .filter(models.Alert.deleted_at == None)
            .offset(skip).limit(limit).all())


def get_alert(db: Session, alert_id: int):
    return db.query(models.Alert).filter(models.Alert.id == alert_id,
                                         models.Alert.deleted_at == None).first()


def create_alert(db: Session, alert: schemas.AlertCreate):
    print(alert)
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def update_alert(db: Session, alert_id: int, alert: schemas.AlertCreate):
    db_alert = db.query(models.Alert).filter(
        models.Alert.id == alert_id,
        models.Alert.deleted_at == None
    ).first()
    if db_alert is None:
        return None
    db_alert.name = alert.name
    db_alert.description = alert.description
    db_alert.period = alert.period
    db_alert.hour = alert.hour
    db_alert.minute = alert.minute
    db_alert.type_alert_id = alert.type_alert_id
    db_alert.updated_at = get_datetime_now()
    db.commit()
    db.refresh(db_alert)
    return db_alert


def delete_alert(db: Session, alert_id: int):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    db_alert.status = "deleted"
    db_alert.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_alert)
    return {
        "status": "success",
        "message": "Alert deleted successfully"
    }


def create_alert_by_type_alert(db: Session, alert: schemas.AlertCreate, type_alert_id: int):
    db_alert = models.Alert(**alert.dict(), type_alert_id=type_alert_id)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def create_type_alert(db: Session, type_alert: schemas.TypeAlertCreate):
    db_type_alert = models.TypeAlert(**type_alert.dict())
    db.add(db_type_alert)
    db.commit()
    db.refresh(db_type_alert)
    return db_type_alert


def get_type_alerts(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.TypeAlert)
            .filter(models.TypeAlert.deleted_at == None)
            .offset(skip).limit(limit).all())


def get_type_alert(db: Session, type_alert_id: int):
    return db.query(models.TypeAlert).filter(models.TypeAlert.id == type_alert_id,
                                             models.TypeAlert.deleted_at == None).first()


def update_type_alert(db: Session, type_alert_id: int, type_alert: schemas.TypeAlertCreate):
    db_type_alert = db.query(models.TypeAlert).filter(
        models.TypeAlert.id == type_alert_id,
        models.TypeAlert.deleted_at == None
    ).first()
    if db_type_alert is None:
        return None
    db_type_alert.name = type_alert.name
    db_type_alert.description = type_alert.description
    db_type_alert.updated_at = get_datetime_now()
    db.commit()
    db.refresh(db_type_alert)
    return db_type_alert


def delete_type_alert(db: Session, type_alert_id: int):
    db_type_alert = db.query(models.TypeAlert).filter(models.TypeAlert.id == type_alert_id).first()
    db_type_alert.status = "deleted"
    db_type_alert.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_type_alert)
    return {
        "status": "success",
        "message": "Type Alert deleted successfully"
    }
