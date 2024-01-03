from fastapi import APIRouter, Depends, HTTPException
from app.sql_app import schemas
from app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session
from app.sql_app.crud import alerts as crud

router = APIRouter()


@router.post("/type_alert/{type_alert_id}/alerts", response_model=schemas.Alert)
def create_alert_for_type_alert(
        type_alert_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)
):
    return crud.create_alert_by_type_alert(db=db, alert=alert, type_alert_id=type_alert_id)


@router.get("/alert/", response_model=list[schemas.Alert])
def read_alert(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = crud.get_alerts(db, skip=skip, limit=limit)
    return alerts


@router.get("/alert/{alert_id}", response_model=schemas.Alert)
def read_alert_by_id(alert_id: int, db: Session = Depends(get_db)):
    alert = crud.get_alert(db, alert_id=alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/alert/{alert_id}", response_model=schemas.Alert)
def update_alert(alert_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    alert = crud.update_alert(db, alert_id=alert_id, alert=alert)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.delete("/alert/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = crud.delete_alert(db, alert_id=alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
