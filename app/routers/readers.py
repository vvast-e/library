from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_active_user
from app.crud.reader import (create_reader, delete_reader, get_reader,
                             get_readers, update_reader)
from app.database import get_db
from app.models.user import User
from app.schemas.reader import ReaderCreate, ReaderResponse, ReaderUpdate

router = APIRouter(prefix="/readers", tags=["readers"])


@router.post("/", response_model=ReaderResponse)
def create(
    reader: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_reader(db, reader)


@router.get("/", response_model=list[ReaderResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_readers(db)


@router.get("/{reader_id}", response_model=ReaderResponse)
def get_one(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return db_reader


@router.put("/update/{reader_id}", response_model=ReaderResponse)
def update(
    reader_id: int,
    reader: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_reader = update_reader(db, reader_id, reader)
    if not db_reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return db_reader


@router.delete("/")
def delete(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    delete = delete_reader(db, reader_id)
    if not delete:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return delete
