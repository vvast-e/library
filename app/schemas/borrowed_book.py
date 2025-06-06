from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BorrowedBookBase(BaseModel):
    book_id: int
    reader_id: int


class BorrowedBookCreate(BorrowedBookBase):
    pass


class BorrowedBookUpdate(BorrowedBookBase):
    return_date: Optional[datetime] = None


class BorrowedBookResponse(BorrowedBookBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime]

    class Config:
        from_attributes = True
