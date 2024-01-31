from sqlalchemy.orm import Session
from src.app.sql_app.models import Task


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks_by_ids(self, task_ids: list[int]) -> list[Task]:
        return self.db.query(Task).filter(
            Task.deleted_at == None,
            Task.id.in_(task_ids)
        ).all()
