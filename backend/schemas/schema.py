from pydantic import BaseModel, Field, PositiveInt, field_validator
from enum import Enum
from typing import Optional, List

import datetime
import re

class LoginSchema(BaseModel):
    username: str
    password: str


class Role(str, Enum):
    STUDENT = "student"
    LIBRARIAN = "librarian"
    ANONYMOUS = "anonymous"


class BookBase(BaseModel):
    title: str = Field(description="Title of the book")
    total_copies: PositiveInt = Field(description="Total number of copies of the book")

class BookCreate(BookBase):
    available_copies: Optional[PositiveInt] = Field(
        description="Number of copies of the book currently available"
    )

class Book(BookBase):
    book_id: PositiveInt = Field(description="Unique identifier for the book")

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str = Field(
        min_length=4, 
        pattern="^[A-Za-z0-9_]+$",
        description="Username of the user",
        examples=["username"]
    )
    userrole: Role = Field(
        Role.STUDENT,
        description="Role of the user (student, librarian, or anonymous)"
    )

class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be 8 characters and contain at least one uppercase letter, "
                    "one lowercase letter, one number, and one special character from '!@#$%^&*()'.",
        examples=["password"]
    )

    @field_validator("password")
    def password_rules(cls, value):
        pattern = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])(?!.*\s)"
        )

        if not pattern.match(value):
            raise ValueError(
                "Password must be 8 characters and contain at least one uppercase letter, "
                "one lowercase letter, one number, and one special character from '!@#$%^&*()'."
            )
        return value

class User(UserBase):
    user_id: PositiveInt = Field(description="Unique identifier for the user")

    class Config:
        from_attributes = True

class BorrowingHistoryBase(BaseModel):
    borrow_date: datetime.datetime = Field(
        description="Date and time when the book was borrowed"
    )
    return_date: Optional[datetime.datetime] = Field(
        None,
        description="Date and time when the book was returned"
    )
    reissued: bool = Field(description="Whether the book was reissued or not")
    returned: bool = Field(description="Whether the book was returned or not")

class BorrowingHistoryCreate(BorrowingHistoryBase):
    user_id: PositiveInt = Field(description="User Id of the borrower")

class BorrowingHistory(BorrowingHistoryBase):
    borrow_id: PositiveInt = Field(description="Unique identifier for the borrowing")
    user: User = Field(description="User who borrowed the book")

    class Config:
        from_attributes = True

class BorrowingDetails(BaseModel):
    book_ids: List[PositiveInt] = Field(description="List of books Id of borrowed book", min_length=1, max_length=10)