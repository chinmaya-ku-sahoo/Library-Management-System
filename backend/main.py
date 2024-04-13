from fastapi import FastAPI


from routes import create_table, users, books, students

app = FastAPI(
    title="Library Management System",
    docs_url="/documentation",
    description="Library Management System for managing"
    )

app.include_router(create_table.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(students.router)