from sqlalchemy.orm import Session

from src.app.helpers import get_datetime_now
from src.app.sql_app import models, schemas


def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Alert)
            .filter(models.Alert.deleted_at == None)
            .offset(skip).limit(limit).all())


def get_alert(db: Session, alert_id: int):
    return db.query(models.Alert).filter(models.Alert.id == alert_id,
                                         models.Alert.deleted_at == None).first()


def create_alert(db: Session, alert: schemas.AlertCreate):
    print(alert)
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def update_alert(db: Session, alert_id: int, alert: schemas.AlertCreate):
    db_alert = db.query(models.Alert).filter(
        models.Alert.id == alert_id,
        models.Alert.deleted_at == None
    ).first()
    if db_alert is None:
        return None
    db_alert.name = alert.name
    db_alert.description = alert.description
    db_alert.period = alert.period
    db_alert.hour = alert.hour
    db_alert.minute = alert.minute
    db_alert.type_alert_id = alert.type_alert_id
    db_alert.updated_at = get_datetime_now()
    db.commit()
    db.refresh(db_alert)
    return db_alert


def delete_alert(db: Session, alert_id: int):
    db_alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    db_alert.status = "deleted"
    db_alert.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_alert)
    return {
        "status": "success",
        "message": "Alert deleted successfully"
    }


def create_alert_by_type_alert(db: Session, alert: schemas.AlertCreate, type_alert_id: int):
    db_alert = models.Alert(**alert.model_dump(exclude={"type_alert_id"}), type_alert_id=type_alert_id)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert
