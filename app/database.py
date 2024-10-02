from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#Purpose: This line creates a connection to the database.

#create_engine: A function from SQLAlchemy that establishes a connection to the database 
# using the provided database URL.

#SQLALCHEMY_DATABASE_URL: A string that contains the database URL, which typically includes the database type 
# (e.g., PostgreSQL, MySQL, SQLite), username, password, host, port, and database name.

#Result: The engine object acts as the core interface for interacting with the database. It handles the actual connection pool and allows SQLAlchemy to execute SQL queries

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Purpose: This line sets up a factory for creating new database session objects.

#sessionmaker: A SQLAlchemy function that creates a new class for sessions. 
# Sessions are used to manage connections to the database,
#  and they handle transactions (grouping multiple database operations into a single, atomic unit).

#autocommit=False: By default, this ensures that each session requires an explicit commit (session.commit()) to save changes 
# to the database, which is important for transaction control.

#autoflush=False: This prevents automatic flushing of the session’s pending changes to the database before each query.
#  Flushing refers to synchronizing the changes made in the session with the database. You typically flush manually by 
# calling session.flush() or session.commit().

#bind=engine: Associates the session with the previously created engine, meaning that this session will use the same database connection configuration.

#Result: SessionLocal becomes a factory function for creating new sessions. Whenever you need to interact with the database, you can instantiate a new session by calling session = SessionLocal().


Base = declarative_base()

#Purpose: This line creates a base class for your ORM models.

#declarative_base(): A function in SQLAlchemy that returns a base class.
#You use this base class to define your ORM models by subclassing it.

#Result: Base is now the base class that you’ll use for all your model classes.

#Each model class will inherit from Base, and SQLAlchemy will use this to map the classes to database tables.

#Summary of Use:
#engine: Manages the database connection.
#SessionLocal: Provides sessions to interact with the database, controlling transactions and queries.
#Base: Serves as the foundation for defining database models, linking Python classes to database tables.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()