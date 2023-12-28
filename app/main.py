from fastapi import FastAPI

from app.sql_app import models
from app.sql_app.database import engine
from app.routers import users, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Implementing the APIRouter

app.include_router(users.router)
app.include_router(tasks.router)
