import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db import SessionLocal, create_tables
from db.crud import create_category, create_book

def main():
    print(" Начинаем инициализацию базы данных...")
    
    # 1. Создаем таблицы
    create_tables()
    
    # 2. Создаем сессию для работы с БД
    db = SessionLocal()
    
    try:
        print(" Добавляем категории...")
        
        # 3. Добавляем 2 категории
        cat1 = create_category(db, "Художественная литература")
        cat2 = create_category(db, "Техническая литература")
        print(f" Добавлены категории: {cat1.title}, {cat2.title}")
        
        print(" Добавляем книги в первую категорию...")
        
        # 4. Добавляем 3 книги в первую категорию
        create_book(db, "Война и мир", 1200.50, cat1.id, 
                   "Роман Льва Толстого", "https://example.com/book1")
        create_book(db, "Преступление и наказание", 850.00, cat1.id,
                   "Роман Достоевского", "https://example.com/book2")
        create_book(db, "Мастер и Маргарита", 950.00, cat1.id,
                   "Роман Булгакова", "https://example.com/book3")
        print(" Добавлено 3 книги в первую категорию")
        
        print(" Добавляем книги во вторую категорию...")
        
        # 5. Добавляем 4 книги во вторую категорию
        create_book(db, "Python для начинающих", 1500.00, cat2.id,
                   "Учебник по Python", "https://example.com/book4")
        create_book(db, "Чистый код", 1800.00, cat2.id,
                   "Книга о программировании", "https://example.com/book5")
        create_book(db, "Алгоритмы", 2000.00, cat2.id,
                   "Книга об алгоритмах", "https://example.com/book6")
        create_book(db, "Базы данных", 1700.00, cat2.id,
                   "Учебник по SQL", "https://example.com/book7")
        print(" Добавлено 4 книги во вторую категорию")
        
        print("\n Инициализация завершена успешно!")
        print(f"   Всего: 2 категории, 7 книг")
        
    except Exception as e:
        print(f" Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()