from fastapi import APIRouter, Depends, HTTPException

from src.app.services.tasks import TaskService
from src.app.sql_app import schemas
from src.app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session
from src.app.sql_app.crud import histories as crud

router = APIRouter()


@router.post("/history/{owner_id}", response_model=schemas.History)
def create_history(
        owner_id: int, history: schemas.HistoryCreate, db: Session = Depends(get_db)
):
    return crud.create_history_by_user(db=db, history=history, owner_id=owner_id)


@router.get("/histories/", response_model=list[schemas.History])
def read_histories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Refactor this to a service
    task_service = TaskService(db)
    task_service.update_tasks_to_repeat_type(1)
    histories = crud.get_histories(db, skip=skip, limit=limit)
    # Update added minutes to history
    for history in histories:
        added_minutes = 0
        tasks = [task for task in history.tasks if task.repeated_date != None]
        for task in tasks:
            added_minutes += task.minutes_expected * task.repeated_days
        history.added_minutes = added_minutes
    return histories


@router.get("/history/{history_id}", response_model=schemas.History)
def read_history_by_id(history_id: int, db: Session = Depends(get_db)):
    history = crud.get_history(db, history_id=history_id)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history


@router.put("/history/{history_id}", response_model=schemas.History)
def update_history(history_id: int, history: schemas.HistoryUpdate, db: Session = Depends(get_db)):
    history = crud.update_history(db, history_id=history_id, history=history)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history


@router.delete("/history/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history = crud.delete_history(db, history_id=history_id)
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history
