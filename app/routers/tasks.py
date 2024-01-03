from http.client import HTTPException

from fastapi import APIRouter, Depends

from app.sql_app import schemas, crud
from app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users/{user_id}/tasks/", response_model=schemas.Task)
def create_item_for_user(
        user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_user_task(db=db, task=task, user_id=user_id)


@router.get("/task/", response_model=list[schemas.Task])
def read_task(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.get("/task/{task_id}", response_model=schemas.Task)
def read_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/task/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id=task_id, task=task)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
