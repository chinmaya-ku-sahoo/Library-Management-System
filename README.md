# Library Management System

This repository contains the code for a Library Management System, which includes functionality for managing books, users, borrowing history, and renewals in a library setting.

## Installation

To run the application, you'll need to have Python 3.x and all the libraries listed in `requirements.txt` installed.

1. Clone the repository and install the required libraries:
    ```bash
    git clone https://github.com/chinmaya-ku-sahoo/Library-Management-System
    cd Library-Management-System
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    cd backend
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The application should now be running.

## Access URLs
1. http://localhost:8000/docs - API documentation using Swagger
2. http://localhost:8000/redocs - API documentation using ReDoc

## API Endpoints and Descriptions
1. **POST /create-table** - Test Connection and create the database and tables
2. **POST /login** - Login using username and password
3. **GET /users** - Get all user list
4. **POST /users** - Create a new user
5. **GET /books** - Get all book list
6. **POST /books** - Register a new book
7. **GET /library/books** - View books, history, and transactions based on user role
8. **POST /library/borrow** - Borrow books based on book ID
9. **PUT /library/renew/{borrow_id}** - Renew books using borrow ID
10. **DELETE /library/return/{borrow_id}** - Return books using borrow ID

