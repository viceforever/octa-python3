# octa-python3

# Для запуска API необходимо:
1) Активировать виртуальное окружение командой source venv/bin/activate
2) Запустить сервер командой uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Сервер будет доступен по адресу: http://127.0.0.1:8000

# После запуска доступны:
* Swagger UI (интерактивная документация): http://127.0.0.1:8000/docs
* ReDoc (альтернативная документация): http://127.0.0.1:8000/redoc
* Health check: http://127.0.0.1:8000/health

# Основные эндпоинты:
Категории:
* GET /categories - список всех категорий
* GET /categories/{id} - категория по ID
* POST /categories - создать категорию
* PUT /categories/{id} - обновить категорию
* DELETE /categories/{id} - удалить категорию

Книги:
* GET /books - список всех книг
* GET /books/{id} - книга по ID
* POST /books - создать книгу
* PUT /books/{id} - обновить книгу
* DELETE /books/{id} - удалить книгу

Фильтрация книг:
* GET /books?category_id=1 - книги по категории
* GET /books?search=python - поиск по названию

# Для Тестирования API через Swagger:
1) Откройте http://127.0.0.1:8000/docs
2) Разверните нужный эндпоинт
3) Нажмите "Try it out"
4) Введите данные и нажмите "Execute"

# Проверка данных в БД:
1) Подключиться к PostgreSQL: PGPASSWORD=12345 psql -U octagon -d octagon_db -h localhost
2) Проверить данные SQL запросами (например, SELECT * FROM categories)