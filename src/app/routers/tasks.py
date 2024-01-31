from fastapi import APIRouter, Depends, HTTPException

from src.app.sql_app import schemas
from src.app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session
from src.app.sql_app.crud import tasks as crud

router = APIRouter()


@router.post("/histories/{history_id}/tasks/", response_model=schemas.Task)
def create_item_for_history(
        history_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_history_task(db=db, task=task, history_id=history_id)


@router.get("/tasks/", response_model=list[schemas.Task])
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
