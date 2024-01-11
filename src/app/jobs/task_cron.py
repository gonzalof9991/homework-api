from typing import List
from src.app.sql_app.crud import tasks as crud
from apscheduler.schedulers.background import BackgroundScheduler
from src.app.sql_app.database import SessionLocal
from src.app.sql_app.models import Task
from src.app.helpers.date import compare_max_date

db = SessionLocal()


def verify_task_defeated():
    tasks_defeated: List[Task] = [task for task in crud.get_tasks(db) if
                                  compare_max_date(task.expiration_date) and task.defeated != 1]
    for task in tasks_defeated:
        task.defeated = 1
        print(task.title)
        print("Send email")
        db.add(task)

    db.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(verify_task_defeated, 'cron', hour=00, minute=00)
# scheduler.add_job(verify_task_defeated, 'interval', seconds=3)
