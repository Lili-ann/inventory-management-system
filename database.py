from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# The connection string to your Dockerized Postgres database
# This uses the credentials from your docker-compose.yml
SQLALCHEMY_DATABASE_URL = "postgresql://lili:lilian17@localhost:5422/inventory_db"

# Create the SQLAlchemy "engine" (the core bridge to the database)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory to actually talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our data models
Base = declarative_base()