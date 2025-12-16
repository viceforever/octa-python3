from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Category(Base):
    """Таблица категорий"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    
    # Связь с книгами (одна категория - много книг)
    books = relationship("Book", back_populates="category")

class Book(Base):
    """Таблица книг"""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    url = Column(String(500))
    
    # Ссылка на категорию (внешний ключ)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Связь с категорией
    category = relationship("Category", back_populates="books")