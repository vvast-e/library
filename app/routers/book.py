from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_active_user
from app.crud.book import (create_book, delete_book, get_book, get_books,
                           get_by_author, update_book)
from app.database import get_db
from app.models.user import User
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse)
def create(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_book(db, book)


@router.get("/", response_model=list[BookResponse])
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def read_one(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book


@router.get("/search/author/{author}", response_model=list[BookResponse])
def read_author(
    author: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_book = get_by_author(db, author)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книги не найдены")
    return get_by_author(db, author)


@router.put("/{book_id}", response_model=BookResponse)
def update(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    updated = update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return updated


@router.delete("/{book_id}")
def delete(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = delete_book(db, book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return result
