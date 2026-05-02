from fastapi import FastAPI
import item
from database import engine

# tells SQLAlchemy to log into Postgres and create your tables!
item.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="Inventory Management System")

# A simple GET endpoint to test that the server is running
@app.get("/")
def root():
    return {"message": "Welcome to Lilian's Inventory Management System! She has successfully connected the database"}