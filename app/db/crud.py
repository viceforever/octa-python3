from sqlalchemy.orm import Session
from . import models

# ========== CRUD для Category ==========
def create_category(db: Session, title: str):
    """Создать категорию"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    """Получить все категории"""
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int):
    """Получить категорию по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def update_category(db: Session, category_id: int, new_title: str):
    """Обновить название категории"""
    category = get_category(db, category_id)
    if category:
        category.title = new_title
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    """Удалить категорию"""
    category = get_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

# ========== CRUD для Book ==========
def create_book(db: Session, title: str, price: float, category_id: int, 
                description: str = None, url: str = None):
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

def get_books(db: Session):
    """Получить все книги"""
    return db.query(models.Book).all()

def get_book(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int):
    """Получить книги по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def update_book(db: Session, book_id: int, **kwargs):
    """Обновить книгу"""
    book = get_book(db, book_id)
    if book:
        for key, value in kwargs.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False