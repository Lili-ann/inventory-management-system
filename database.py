from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# The connection string to your Dockerized Postgres database
# Notice we changed 'localhost:5422' to 'inventory_postgres:5432' for internal Docker networking
SQLALCHEMY_DATABASE_URL = "postgresql://lili:lilian17@inventory_postgres:5432/inventory_db"

# Create the SQLAlchemy "engine" (the core bridge to the database)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory to actually talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our data models
Base = declarative_base()