from fastapi import APIRouter, Depends, HTTPException
from app.sql_app import schemas, crud
from app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/type_alert/", response_model=schemas.TypeAlert)
def create_type_alert(
        type_alert: schemas.TypeAlertCreate, db: Session = Depends(get_db)
):
    return crud.create_type_alert(db=db, type_alert=type_alert)


@router.get("/type_alert/", response_model=list[schemas.TypeAlert])
def read_type_alert(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    type_alerts = crud.get_type_alerts(db, skip=skip, limit=limit)
    return type_alerts


@router.get("/type_alert/{type_alert_id}", response_model=schemas.TypeAlert)
def read_type_alert_by_id(type_alert_id: int, db: Session = Depends(get_db)):
    type_alert = crud.get_type_alert(db, type_alert_id=type_alert_id)
    if type_alert is None:
        raise HTTPException(status_code=404, detail="Type Alert not found")
    return type_alert


@router.put("/type_alert/{type_alert_id}", response_model=schemas.TypeAlert)
def update_type_alert(type_alert_id: int, type_alert: schemas.TypeAlertCreate, db: Session = Depends(get_db)):
    type_alert = crud.update_type_alert(db, type_alert_id=type_alert_id, type_alert=type_alert)
    if type_alert is None:
        raise HTTPException(status_code=404, detail="Type Alert not found")
    return type_alert


@router.delete("/type_alert/{type_alert_id}")
def delete_type_alert(type_alert_id: int, db: Session = Depends(get_db)):
    type_alert = crud.delete_type_alert(db, type_alert_id=type_alert_id)
    if type_alert is None:
        raise HTTPException(status_code=404, detail="Type Alert not found")
    return type_alert
