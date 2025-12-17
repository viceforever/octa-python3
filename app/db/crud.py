from sqlalchemy.orm import Session
from typing import List, Optional
from . import models


# ========== CRUD для Category ==========

def create_category(db: Session, title: str) -> models.Category:
    """Создать категорию"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """Получить все категории с пагинацией"""
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """Получить категорию по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_title(db: Session, title: str) -> Optional[models.Category]:
    """Получить категорию по названию"""
    return db.query(models.Category).filter(models.Category.title == title).first()


def update_category(db: Session, category_id: int, title: str) -> Optional[models.Category]:
    """Обновить название категории"""
    category = get_category(db, category_id)
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    """Удалить категорию"""
    category = get_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
        return True
    return False


# ========== CRUD для Book ==========

def create_book(
    db: Session, 
    title: str, 
    price: float, 
    category_id: Optional[int] = None,
    description: Optional[str] = None,
    url: Optional[str] = None
) -> models.Book:
    """Создать книгу"""
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Book]:
    """Получить все книги с пагинацией"""
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books_by_category(db: Session, category_id: int) -> List[models.Book]:
    """Получить книги по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()


def search_books_by_title(db: Session, search_term: str) -> List[models.Book]:
    """Поиск книг по названию"""
    return db.query(models.Book).filter(
        models.Book.title.ilike(f"%{search_term}%")
    ).all()


def update_book(
    db: Session, 
    book_id: int, 
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    url: Optional[str] = None,
    category_id: Optional[int] = None
) -> Optional[models.Book]:
    """Обновить книгу"""
    book = get_book(db, book_id)
    if book:
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        if price is not None:
            book.price = price
        if url is not None:
            book.url = url
        if category_id is not None:
            book.category_id = category_id
        
        db.commit()
        db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    """Удалить книгу"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False