from sqlalchemy.orm import Session

from src.app.helpers import get_datetime_now
from src.app.sql_app.models import Task


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks_by_ids(self, task_ids: list[int]) -> list[Task]:
        return self.db.query(Task).filter(
            Task.deleted_at == None,
            Task.id.in_(task_ids)
        ).all()

    def update_tasks_to_repeat_type(self, repeat: int):
        now = get_datetime_now()
        tasks = self.db.query(Task).filter(
            Task.deleted_at is None,
            Task.repeat is repeat,
            Task.repeated_date is not now
        ).all()
        # If there are no tasks to update, return
        if len(tasks) == 0:
            return
        # Update tasks
        for task in tasks:
            task.type = 0  # reset task type -> New
            task.minutes_completed = 0
            task.repeated_date = now
            if task.repeated_days is None:
                task.repeated_days = 1
            else:
                task.repeated_days = task.repeated_days + 1
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
