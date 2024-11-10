# API Development with Python updated version (Based on FreeCodeCamp Tutorial)

I followed the first 11 hours of the [FreeCodeCamp API development tutorial](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41400s) to learn about building APIs with Python. This repository contains my work, which may differ slightly from the tutorial.

Some functions used in the tutorial no longer exist, so I adapted parts of the code while maintaining the original function signatures and outputs. If you're looking for alternative approaches or inspiration beyond the tutorial, you can explore my implementations here.

## Technologies Used

### Software:
- **Postman** - API testing and development tool.
- **PostgreSQL** - Relational database management system.

### Libraries:
- **FastAPI** - Web framework for building APIs with Python.
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping (ORM) library.
- **Alembic** - Lightweight database migration tool for use with SQLAlchemy.

### Techniques:
- **CRUD Operations** - Implementation of Create, Read, Update, Delete operations.

Here’s the README content for running the project locally:

---



## How to Run Locally

### Step 1: Clone the Repository

First, clone this repository using the following command:

```bash
git clone https://github.com/AffesRoua/Python-API-Development--updated-version---FreeCodeCamp.git
```

### Step 2: Navigate to the Project Directory

Move into the project directory:

```bash
cd Python-API-Development--updated-version---FreeCodeCamp
```

### Step 3: Install FastAPI with All Dependencies

Install FastAPI using the `[all]` flag:

```bash
pip install fastapi[all]
```

### Step 4: Run the Application

From the project directory, run the following command:

```bash
uvicorn main:app --reload
```

You can now access the API documentation through the following link:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Step 5: Set Up a PostgreSQL Database

To use this API, you will need a PostgreSQL database. After creating a database, create a `.env` file in the project folder and add the following environment variables:

```env
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = your_database_password
DATABASE_NAME = your_database_name
DATABASE_USERNAME = your_database_username
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7  # Replace this with a secure key
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

> **Note**: The `SECRET_KEY` provided above is a placeholder. You should generate a secure key for production use. Check the [FastAPI documentation](https://fastapi.tiangolo.com/) for guidance on generating a `SECRET_KEY`.

--- 

This should help set up and run the FastAPI project locally with ease.
