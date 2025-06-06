from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.borrowed_book import BorrowedBook


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    year = Column(Integer)
    isbn = Column(String, unique=True)
    quantity = Column(Integer, default=1)

    borrows = relationship(BorrowedBook, back_populates="book")
