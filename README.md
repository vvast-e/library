# library
 📚 Library Management System API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)

REST API для управления библиотекой с аутентификацией, бизнес-логикой и полным CRUD функционалом.

## 🌟 Особенности

- Полноценная система управления книгами и читателями
- JWT-аутентификация с ролевой моделью
- Бизнес-логика: лимит книг, контроль доступности
- Документированные эндпоинты (Swagger/ReDoc)
- Асинхронная работа с PostgreSQL через SQLAlchemy 2.0
- Автоматические миграции через Alembic

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- PostgreSQL 14+
- Poetry (для управления зависимостями)

bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/library-api.git
cd library-api

# 2. Установить зависимости
poetry install

# 3. Настроить окружение
cp .env.example .env
# Отредактировать .env с вашими данными

# 4. Запустить сервер
poetry run uvicorn app.main:app --reload
После запуска откройте документацию:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🗄 Структура базы данных
https://via.placeholder.com/800x500?text=Database+Schema+Diagram

Основные таблицы:

books - информация о книгах

readers - зарегистрированные читатели

users - учетные записи сотрудников

borrowed_books - журнал выдачи книг

🔐 Аутентификация
Система использует JWT-токены. Пример workflow:

Регистрация библиотекаря:

bash
POST /auth/register
{
  "email": "librarian@example.com",
  "password": "securepassword123"
}
Получение токена:

bash
POST /auth/token
{
  "username": "librarian@example.com",
  "password": "securepassword123"
}
Использование токена:

text
Authorization: Bearer ваш_токен_здесь
📚 Бизнес-правила
Лимит книг: Читатель может иметь не более 3 книг одновременно

Доступность: Книга может быть выдана только если есть доступные экземпляры

Повторная выдача: Нельзя выдать одну книгу читателю дважды без возврата

📊 Примеры запросов
Добавление книги:

bash
POST /books/
{
  "title": "Clean Code",
  "author": "Robert Martin",
  "year": 2008,
  "isbn": "9780132350884",
  "quantity": 5
}
Выдача книги читателю:

bash
POST /borrowed/
{
  "book_id": 1,
  "reader_id": 1
}
🧪 Тестирование
Запуск тестов:

bash
poetry run pytest -v
Тестовое покрытие включает:

Юнит-тесты CRUD операций

Интеграционные тесты API

Проверку бизнес-правил

Тесты безопасности

🛠 Технологический стек
Компонент	Версия	Назначение
FastAPI	0.95+	Веб-фреймворк
SQLAlchemy	2.0+	ORM
Pydantic	2.0+	Валидация данных
Alembic	1.10+	Миграции БД
JWT	0.4+	Аутентификация
pytest	7.3+	Тестирование
