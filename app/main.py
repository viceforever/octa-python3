from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.db import create_tables
from app.api import books, categories
from app.schemas import HealthCheck

# Создаем таблицы при старте приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения...")
    create_tables()
    print("Таблицы созданы/проверены")
    yield
    print("Выключение приложения...")

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Book Store API",
    description="API для управления книгами и категориями",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)


# Health check endpoint
@app.get("/", tags=["health"])
@app.get("/health", tags=["health"])
async def health_check():
    """
    Проверка работоспособности API и подключения к БД
    """
    return HealthCheck()


# Информация о API
@app.get("/info", tags=["info"])
async def api_info():
    """
    Получить информацию о API
    """
    return {
        "name": "Book Store API",
        "version": "1.0.0",
        "description": "API для управления книгами и категориями",
        "endpoints": {
            "categories": "/categories",
            "books": "/books",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )