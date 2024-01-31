from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.app.sql_app import models
from src.app.sql_app.database import engine
from src.app.routers import users, tasks, categories, alerts, types_alerts, histories
from src.app.jobs.task_cron import scheduler

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Implementing the APIRouter

api.include_router(users.router)
api.include_router(tasks.router)
api.include_router(categories.router)
api.include_router(alerts.router)
api.include_router(types_alerts.router)
api.include_router(histories.router)


@api.get("/")
def read_root():
    return {"Hello": "World"}


# Define Cron Jobs
scheduler.start()
