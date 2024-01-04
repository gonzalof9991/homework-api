from fastapi import FastAPI
from app.sql_app import models
from app.sql_app.database import engine
from app.routers import users, tasks, categories, alerts, types_alerts
from app.jobs.task_cron import scheduler

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Implementing the APIRouter

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)
# app.include_router(alerts.router)
# app.include_router(types_alerts.router)

# Define Cron Jobs
scheduler.start()
