from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.book import router as books_router
from app.routers.borrowed_book import router as borrowed_books_router
from app.routers.readers import router as reader_router

app = FastAPI()

app.include_router(books_router)
app.include_router(auth_router)
app.include_router(reader_router)
app.include_router(borrowed_books_router)
