from src.app.sql_app import schemas
from sqlalchemy.orm import Session
from src.app.sql_app.models import Category


class CategoryService:
    def __init__(self, db: Session, task: schemas.TaskCreate, ):
        self.db = db
        self.task = task

    def get_categories_by_names(self, category_names: list[str]):
        return self.db.query(Category).filter(
            Category.deleted_at == None,
            Category.name.in_(category_names)
        ).all()

    def get_categories_by_ids(self, category_ids: list[int]) -> list[Category]:
        return self.db.query(Category).filter(
            Category.deleted_at == None,
            Category.id.in_(category_ids)
        ).all()
