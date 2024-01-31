from sqlalchemy.orm import Session

from src.app.helpers import get_datetime_now
from src.app.services.tasks import TaskService
from src.app.sql_app import models, schemas


def create_history_by_user(db: Session, history: schemas.HistoryCreate, owner_id: int):
    db_history = models.History(**history.model_dump(exclude={"created_at"}), owner_id=owner_id)
    db_history.created_at = get_datetime_now()
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


def get_history(db: Session, history_id: int):
    return db.query(models.History).filter(models.History.id == history_id,
                                           models.History.deleted_at == None).first()


def get_histories(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.History)
            .filter(models.History.deleted_at == None)
            .offset(skip).limit(limit).all())


def update_history(db: Session, history_id: int, history: schemas.HistoryUpdate):
    db_history = db.query(models.History).filter(models.History.id == history_id).first()
    db_history.title = history.title
    db_history.description = history.description
    db_history.owner_id = history.owner_id
    # taskService
    task_service = TaskService(db=db)
    # get tasks by ids
    tasks = task_service.get_tasks_by_ids(task_ids=history.tasks)
    # clear tasks
    db_history.tasks.clear()
    # add tasks
    db_history.tasks.extend(tasks)
    db_history.updated_at = get_datetime_now()
    db.commit()
    db.refresh(db_history)
    return db_history


def delete_history(db: Session, history_id: int):
    db_history = db.query(models.History).filter(models.History.id == history_id).first()
    db_history.status = "deleted"
    db_history.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_history)
    return {
        "status": "success",
        "message": "History deleted successfully"
    }
