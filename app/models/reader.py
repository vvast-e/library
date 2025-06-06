from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Reader(Base):
    __tablename__ = "reader"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    borrows = relationship("BorrowedBook", back_populates="reader")
