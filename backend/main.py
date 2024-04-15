from fastapi import FastAPI


from routers import create_table, users, books, login, borrow, renew, return_book

app = FastAPI(
    title="Library Management System",
    docs_url="/docs",
    redoc_url="/redocs",
    description="Library Management System for managing"
    )

app.include_router(create_table.router)
app.include_router(login.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrow.router)
app.include_router(renew.router)
app.include_router(return_book.router)
