from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ========== Схемы для Category ==========

class CategoryBase(BaseModel):
    """Базовая схема категории"""
    title: str = Field(..., min_length=1, max_length=100, description="Название категории")

class CategoryCreate(CategoryBase):
    """Схема для создания категории"""
    pass

class CategoryUpdate(BaseModel):
    """Схема для обновления категории"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Название категории")

class Category(CategoryBase):
    """Схема ответа для категории"""
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ========== Схемы для Book ==========

class BookBase(BaseModel):
    """Базовая схема книги"""
    title: str = Field(..., min_length=1, max_length=200, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: float = Field(..., gt=0, description="Цена книги (должна быть больше 0)")
    url: Optional[str] = Field(None, max_length=500, description="Ссылка на книгу")
    category_id: Optional[int] = Field(None, description="ID категории")

class BookCreate(BookBase):
    """Схема для создания книги"""
    pass

class BookUpdate(BaseModel):
    """Схема для обновления книги"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    url: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None

class Book(BookBase):
    """Схема ответа для книги"""
    id: int
    created_at: Optional[datetime] = None
    category: Optional[Category] = None  # Вложенная категория
    
    class Config:
        from_attributes = True


# ========== Схемы для ответов API ==========

class HealthCheck(BaseModel):
    """Схема для health check"""
    status: str = "OK"
    database: str = "connected"
    timestamp: datetime = Field(default_factory=datetime.now)

class PaginatedResponse(BaseModel):
    """Схема для пагинированного ответа"""
    total: int
    page: int
    per_page: int
    items: list