from fastapi import FastAPI


from routes import create_table, users

app = FastAPI(
    title="Library Management System",
    docs_url="/documentation",
    description="Library Management System for managing"
    )

app.include_router(create_table.router)
app.include_router(users.router)