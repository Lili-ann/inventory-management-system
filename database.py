from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://lili:lilian17@inventory_postgres:5432/inventory_db"

# Create the SQLAlchemy "engine" 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for data models
Base = declarative_base()