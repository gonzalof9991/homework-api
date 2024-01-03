from sqlalchemy.orm import Session

from app.helpers import get_datetime_now
from app.sql_app import models, schemas


def create_type_alert(db: Session, type_alert: schemas.TypeAlertCreate):
    db_type_alert = models.TypeAlert(**type_alert.dict())
    db.add(db_type_alert)
    db.commit()
    db.refresh(db_type_alert)
    return db_type_alert


def get_type_alerts(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.TypeAlert)
            .filter(models.TypeAlert.deleted_at == None)
            .offset(skip).limit(limit).all())


def get_type_alert(db: Session, type_alert_id: int):
    return db.query(models.TypeAlert).filter(models.TypeAlert.id == type_alert_id,
                                             models.TypeAlert.deleted_at == None).first()


def update_type_alert(db: Session, type_alert_id: int, type_alert: schemas.TypeAlertCreate):
    db_type_alert = db.query(models.TypeAlert).filter(
        models.TypeAlert.id == type_alert_id,
        models.TypeAlert.deleted_at == None
    ).first()
    if db_type_alert is None:
        return None
    db_type_alert.name = type_alert.name
    db_type_alert.description = type_alert.description
    db_type_alert.updated_at = get_datetime_now()
    db.commit()
    db.refresh(db_type_alert)
    return db_type_alert


def delete_type_alert(db: Session, type_alert_id: int):
    db_type_alert = db.query(models.TypeAlert).filter(models.TypeAlert.id == type_alert_id).first()
    db_type_alert.status = "deleted"
    db_type_alert.deleted_at = get_datetime_now()
    db.commit()
    db.refresh(db_type_alert)
    return {
        "status": "success",
        "message": "Type Alert deleted successfully"
    }
