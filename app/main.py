import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db import SessionLocal
from db.crud import get_categories, get_books, get_books_by_category

def display_data():
    print("=" * 60)
    print(" СОДЕРЖИМОЕ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. Получаем все категории
        categories = get_categories(db)
        
        if not categories:
            print("База данных пуста!")
            print("Запустите: python app/init_db.py")
            return
        
        # 2. Выводим категории и книги
        for category in categories:
            print(f"\n КАТЕГОРИЯ: {category.title}")
            print("-" * 40)
            
            # Получаем книги этой категории
            books = get_books_by_category(db, category.id)
            
            if books:
                for book in books:
                    print(f"   {book.title}")
                    print(f"     Цена: {book.price} руб.")
                    print(f"     Описание: {book.description or 'Нет описания'}")
                    print(f"     Ссылка: {book.url or 'Нет ссылки'}")
                    print()
            else:
                print("  Нет книг в этой категории")
        
        # 3. Общая статистика
        print("\n" + "=" * 60)
        print(" СТАТИСТИКА")
        print("-" * 60)
        
        all_books = get_books(db)
        total_books = len(all_books)
        total_price = sum(book.price for book in all_books)
        
        print(f"Всего категорий: {len(categories)}")
        print(f"Всего книг: {total_books}")
        print(f"Общая стоимость всех книг: {total_price:.2f} руб.")
        
        if all_books:
            avg_price = total_price / total_books
            max_price = max(all_books, key=lambda x: x.price)
            min_price = min(all_books, key=lambda x: x.price)
            
            print(f"Средняя цена книги: {avg_price:.2f} руб.")
            print(f"Самая дорогая книга: '{max_price.title}' - {max_price.price} руб.")
            print(f"Самая дешевая книга: '{min_price.title}' - {min_price.price} руб.")
        
        print("=" * 60)
        
    finally:
        db.close()

if __name__ == "__main__":
    display_data()