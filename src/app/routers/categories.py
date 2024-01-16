from typing import List

from fastapi import APIRouter, Depends, HTTPException
from src.app.sql_app import schemas
from src.app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session
from src.app.sql_app.crud import categories as crud
from src.app.sql_app.models import Category

router = APIRouter()


@router.post("/category/", response_model=schemas.Category)
def create_category(
        category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    return crud.create_category(db=db, category=category)


@router.get("/categories/", response_model=list[schemas.CategoryByNameId])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories: List[Category] = crud.get_categories(db, skip=skip, limit=limit)
    names_ids = [{"name": category.name, "id": category.id} for category in categories]
    return names_ids


@router.get("/category/{category_id}", response_model=schemas.Category)
def read_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/category/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = crud.update_category(db, category_id=category_id, category=category)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/category/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.delete_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
