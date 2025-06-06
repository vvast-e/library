from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.book import get_book
from app.models.borrowed_book import BorrowedBook


def create_borrowed_book(db: Session, reader_id: int, book_id: int):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    if book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Нет копий книг")
    count_user_books = get_active_borrows(db, reader_id)
    if count_user_books >= 3:
        raise HTTPException(status_code=400, detail="уже взял 3 книги")
    borrowed_book = get_active_borrows_list(db, reader_id)
    for book_new in borrowed_book:
        if book_new.book_id == book_id:
            raise HTTPException(status_code=400, detail="Книга уже взята")
    db_borrow = BorrowedBook(
        book_id=book_id, reader_id=reader_id, borrow_date=datetime.utcnow()
    )
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)

    book.quantity -= 1
    db.commit()
    db.refresh(book)
    return db_borrow


def get_active_borrows(db: Session, reader_id: int):
    return (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.reader_id == reader_id,
            BorrowedBook.return_date is None)
        .count()
    )


def get_active_borrows_list(db: Session, reader_id: int):
    return (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.reader_id == reader_id,
            BorrowedBook.return_date is None)
        .all()
    )


def return_borrow(db: Session, reader_id: int, book_id: int):
    book = get_book(db, book_id)
    db_borrow = (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.book_id == book_id,
            BorrowedBook.reader_id == reader_id,
            BorrowedBook.return_date is None,
        )
        .first()
    )

    if not db_borrow:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    db_borrow.return_date = datetime.utcnow()
    db.commit()
    db.refresh(db_borrow)

    book.quantity += 1
    db.commit()
    db.refresh(book)
    return db_borrow


def get_borrows_by_reader(db: Session, reader_id: int):
    return (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.reader_id == reader_id,
            BorrowedBook.return_date is None)
        .all()
    )


def get_borrows_by_book(db: Session, book_id: int):
    return (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.book_id == book_id,
            BorrowedBook.return_date is None)
        .all()
    )
