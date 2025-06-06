from pydantic import BaseModel


class ReaderBase(BaseModel):
    name: str
    email: str


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(ReaderBase):
    pass


class ReaderResponse(ReaderBase):
    id: int

    class Config:
        from_attributes: True
