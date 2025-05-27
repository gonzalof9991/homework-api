from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from src.app.sql_app import models
from src.app.sql_app.database import engine
from src.app.routers import users, tasks, categories, alerts, types_alerts, histories
from src.app.jobs.task_cron import scheduler
from src.app.utils.security import auth_user, create_access_token

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Security
# exception handler for authjwt
# in production, you can tweak performance using orjson response
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Implementing the APIRouter


# This dependency makes a post to "/user/token"
# (from a form containing a username and password)
# and returns an access token.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# This endpoint is directed to by any call that has the
# oauth2_dep() dependency:
@api.post("/token")
async def create_token(
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """Get username and password from OAuth form,
        return access token"""
    user = auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@api.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token"""
    return {"token": token}


@api.get("/")
def read_root(token: str = Depends(oauth2_dep)):
    return {"Hello": "World"}


api.include_router(users.router, tags=["users"])
api.include_router(tasks.router)
api.include_router(categories.router)
api.include_router(alerts.router)
api.include_router(types_alerts.router)
api.include_router(histories.router)

# Define Cron Jobs
scheduler.start()

# TODO: Mejorar la seguridad de la API, crear una ruta para el login y otra para el token
