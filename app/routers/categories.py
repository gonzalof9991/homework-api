from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from app.sql_app import schemas, crud
from app.sql_app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/category/", response_model=schemas.Category)
def create_category(
        category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    return crud.create_category(db=db, category=category)


@router.get("/category/", response_model=list[schemas.Category])
def read_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    category = crud.get_categories(db, skip=skip, limit=limit)
    return category


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
