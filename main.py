from fastapi import FastAPI, Depends, HTTPException, Request 
from fastapi.middleware.cors import CORSMiddleware
import datetime 
from mongo import logs_collection 

import sqlalchemy
from sqlalchemy.orm import Session
import table
from database import engine
import bouncer
from database import SessionLocal


# tells SQLAlchemy to log into Postgres and create your tables!
table.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="Inventory Management System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_api_requests(request: Request, call_next):
    # 1. Let the user's request go through and get the response
    response = await call_next(request)

    # 2. Figure out what "Action" they just did based on the Method
    method = request.method
    endpoint = request.url.path
    action = "UNKNOWN"

    if endpoint.startswith("/item"):
        if method == "POST":
            action = "ADD_INVENTORY"
        elif method == "GET":
            # If it's just /items, it's a LIST. If it's /item/123, it's a GET.
            action = "LIST_INVENTORY" if endpoint == "/items" else "GET_INVENTORY"
        elif method == "PUT":
            action = "EDIT_INVENTORY"
        elif method == "DELETE":
            action = "DELETE_INVENTORY"

    # 3. Build the JSON document exactly how your rubric asked
    log_document = {
        "timestamp": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": method,
        "endpoint": endpoint,
        "action": action,
    }

    # 4. Save it to MongoDB (We use try/except so if Mongo crashes, the API still works)
    try:
        # Avoid logging the /docs or /openapi.json traffic
        if not endpoint.startswith("/docs") and not endpoint.startswith("/openapi"):
            logs_collection.insert_one(log_document)
            print(f"Logged to Mongo: {log_document}") # Just to help you see it in the terminal
    except Exception as e:
        print(f"Failed to log to MongoDB: {e}")

    # 5. Return the final response to the user
    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. CREATE: Add a new item (POST /item)
@app.post("/item", response_model=bouncer.ItemResponse)
def create_item(product: bouncer.ItemCreate, db: Session = Depends(get_db)):
    # Create a new database item based on our models.py blueprint
    db_item = table.Item(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    # Add it to the database and save (commit) the changes
    db.add(db_item)
    db.commit()
    db.refresh(db_item) # Refresh to grab the newly generated UUID
    
    return db_item

#2. READ: Get an item by ID (GET /item/{id})
@app.get("/item/{item_id}", response_model=bouncer.ItemResponse)
def read_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(table.Item).filter(table.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# 3. UPDATE: Update an item by ID (PUT /item/{id})
@app.put("/item/{item_id}", response_model=bouncer.ItemResponse)
def update_item(item_id: str, product: bouncer.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(table.Item).filter(table.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update the item's properties
    db_item.name = product.name
    db_item.description = product.description
    db_item.price = product.price
    db_item.stock = product.stock
    
    db.commit()
    db.refresh(db_item)
    
    return db_item

# 4. DELETE: Delete an item by ID (DELETE /item/{id})
@app.delete("/item/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(table.Item).filter(table.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    
    return {"message": "Item deleted successfully"} 


# 5. LIST VIEW: Get all items (GET /items)
@app.get("/items", response_model=list[bouncer.ItemResponse])
def list_items(db: Session = Depends(get_db)):
    return db.query(table.Item).all()
