import datetime

from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Role(str, Enum):
    STUDENT = "student"
    LIBRARIAN = "librarian"
    ANONYMOUS = "anonymous"


class BookBase(BaseModel):
    title: str
    total_copies: int
    available_copies: Optional[int]

class BookCreate(BookBase):
    pass

class Book(BookBase):
    book_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    userrole: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class BorrowingHistoryBase(BaseModel):
    borrow_date: datetime.datetime
    return_date: Optional[datetime.datetime]
    reissued: bool
    returned: bool

class BorrowingHistoryCreate(BorrowingHistoryBase):
    user_id: int
    book_id: int

class BorrowingHistory(BorrowingHistoryBase):
    borrow_id: int
    user: User
    book: Book

    class Config:
        orm_mode = True
