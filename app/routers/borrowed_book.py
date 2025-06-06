from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_active_user
from app.crud.borrowed_book import (create_borrowed_book, get_borrows_by_book,
                                    get_borrows_by_reader, return_borrow)
from app.database import get_db
from app.models.user import User
from app.schemas.borrowed_book import BorrowedBookResponse, BorrowedBookUpdate

router = APIRouter(prefix="/borrowed", tags=["borrowed"])


@router.post("/borrow", response_model=BorrowedBookResponse)
def create(
    borrowed_book: BorrowedBookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_borrowed_book(db,
                                borrowed_book.reader_id,
                                borrowed_book.book_id
                                )


@router.post("/return", response_model=BorrowedBookResponse)
def return_book(
    borrowed_book: BorrowedBookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return return_borrow(db, borrowed_book.reader_id, borrowed_book.book_id)


@router.get("/readers/{reader_id}", response_model=List[BorrowedBookResponse])
def get_borrows_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_borrows_by_reader(db, reader_id)


@router.get("/books/{book_id}", response_model=List[BorrowedBookResponse])
def get_borrows_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_borrows_by_book(db, book_id)
