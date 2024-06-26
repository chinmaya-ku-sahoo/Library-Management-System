from fastapi import FastAPI


from routers import create_table, users, books, login, borrow, renew, return_book, borrow_history

app = FastAPI(
    title="Library Management System",
    docs_url="/docs",
    redoc_url="/redocs",
    description="The 'Library Management System' includes functionality for \
        managing books, users, borrowing history, and renewals in a library setting."
    )

app.include_router(create_table.router)
app.include_router(login.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrow.router)
app.include_router(renew.router)
app.include_router(return_book.router)
app.include_router(borrow_history.router)
