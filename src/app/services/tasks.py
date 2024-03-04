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
        # now = "2024-02-05"
        tasks = self.db.query(Task).filter(
            Task.deleted_at == None,  # If the task is not deleted
            Task.repeat == repeat,
            Task.type == 2  # Task type = 2 -> Closed
        ).all() or []
        # New filter to get tasks that are not repeated yet or the repeated date is different from today
        tasks = list(filter(lambda task: task.repeated_date is None or task.repeated_date != now, tasks))
        # If there are no tasks to update, return
        if len(tasks) == 0:
            print("No tasks to update")
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

            task.minutes_total = task.minutes_expected * task.repeated_days
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
