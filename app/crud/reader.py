from sqlalchemy.orm import Session

from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate


def get_reader(db: Session, id: int):
    return db.query(Reader).filter(Reader.id == id).first()


def get_readers(db: Session, skip: int = 0, limit: int = 30):
    return db.query(Reader).offset(skip).limit(limit)


def create_reader(db: Session, reader: ReaderCreate):
    db_reader = Reader(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


def update_reader(db: Session, reader_id: int, reader_update: ReaderUpdate):
    reader = get_reader(db, reader_id)
    if not reader:
        return None
    for key, value in reader_update.dict(exclude_unset=True).items():
        setattr(reader, key, value)

    db.commit()
    db.refresh(reader)
    return reader


def delete_reader(db: Session, reader_id: int):
    reader = get_reader(db, reader_id)
    if not reader:
        return None
    db.delete(reader)
    db.commit()
    return {"message": "Читатель удален"}
