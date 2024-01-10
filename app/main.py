from fastapi import FastAPI
from app.sql_app import models
from app.sql_app.database import engine
from app.routers import users, tasks, categories, alerts, types_alerts
from app.jobs.task_cron import scheduler

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

# Implementing the APIRouter

api.include_router(users.router)
api.include_router(tasks.router)
api.include_router(categories.router)
api.include_router(alerts.router)
api.include_router(types_alerts.router)


@api.get("/")
def read_root():
    return {"Hello": "World"}


# Define Cron Jobs
scheduler.start()
