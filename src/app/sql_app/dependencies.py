from src.app.sql_app.database import SessionLocal


# Dependencia para usar en las rutas.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
