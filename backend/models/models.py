from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from connect_db import Base

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    total_copies = Column(Integer)
    available_copies = Column(Integer)

    borrow_history = relationship("BorrowingHistory", back_populates="book")

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    userrole = Column(String)
    password = Column(String)

    borrow_history = relationship("BorrowingHistory", back_populates="user")

class BorrowingHistory(Base):
    __tablename__ = 'borrowing_history'
    borrow_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    borrow_date = Column(DateTime)
    return_date = Column(DateTime)
    reissued = Column(Boolean)
    returned = Column(Boolean)

    user = relationship("User", back_populates="borrow_history")
    book = relationship("Book", back_populates="borrow_history")

# class Renewals(Base):
#     __tablename__ = 'renewals'
#     renewal_id = Column(Integer, primary_key=True)
#     borrow_id = Column(Integer, ForeignKey('borrowing_history.borrow_id'))
#     renewal_date = Column(DateTime)

#     borrowing_history = relationship("BorrowingHistory", back_populates="renewal")

#     __table_args__ = (
#         {"unique_together": ('borrow_id', 'renewal_date')}
#     )
