from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[Category])
def read_categories(
    skip: int = Query(0, ge=0, description="Пропустить первые N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех категорий
    """
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить категорию по ID
    """
    category = crud.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую категорию
    """
    # Проверяем, нет ли уже категории с таким названием
    existing_category = crud.get_category_by_title(db, title=category.title)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория с названием '{category.title}' уже существует"
        )
    
    return crud.create_category(db=db, title=category.title)


@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить категорию
    """
    category = crud.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Если пытаемся изменить название, проверяем уникальность
    if category_update.title is not None:
        existing = crud.get_category_by_title(db, title=category_update.title)
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категория с названием '{category_update.title}' уже существует"
            )
    
    return crud.update_category(
        db=db, 
        category_id=category_id, 
        title=category_update.title
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить категорию
    """
    category = crud.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Проверяем, есть ли книги в этой категории
    books_in_category = crud.get_books_by_category(db, category_id=category_id)
    if books_in_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невозможно удалить категорию, в которой есть книги. "
                   f"Сначала удалите {len(books_in_category)} книг(и) из этой категории."
        )
    
    crud.delete_category(db=db, category_id=category_id)
    return None