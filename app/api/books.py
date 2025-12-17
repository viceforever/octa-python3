from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import Book, BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[Book])
def read_books(
    skip: int = Query(0, ge=0, description="Пропустить первые N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    search: Optional[str] = Query(None, description="Поиск по названию книги"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех книг
    - **category_id**: Фильтр по категории
    - **search**: Поиск по названию книги
    """
    if search:
        books = crud.search_books_by_title(db, search_term=search)
    elif category_id is not None:
        books = crud.get_books_by_category(db, category_id=category_id)
    else:
        books = crud.get_books(db, skip=skip, limit=limit)
    
    return books


@router.get("/{book_id}", response_model=Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить книгу по ID
    """
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую книгу
    """
    # Проверяем существование категории, если указана
    if book.category_id is not None:
        category = crud.get_category(db, category_id=book.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {book.category_id} не найдена"
            )
    
    return crud.create_book(
        db=db,
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url,
        category_id=book.category_id
    )


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить книгу
    """
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    # Проверяем существование категории, если указана
    if book_update.category_id is not None:
        category = crud.get_category(db, category_id=book_update.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {book_update.category_id} не найдена"
            )
    
    return crud.update_book(
        db=db,
        book_id=book_id,
        title=book_update.title,
        description=book_update.description,
        price=book_update.price,
        url=book_update.url,
        category_id=book_update.category_id
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить книгу
    """
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    crud.delete_book(db=db, book_id=book_id)
    return None