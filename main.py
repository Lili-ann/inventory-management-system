from fastapi import FastAPI, Depends, HTTPException, Request 
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import datetime 
from mongo import logs_collection 

import sqlalchemy
from sqlalchemy.orm import Session
import table
from database import engine
import bouncer
from database import SessionLocal


#SQLAlchemy log into Postgres and create tables!
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
    #Let the user's request go through and get the response
    response = await call_next(request)

    #identify user action based on the endpoint and method
    method = request.method
    endpoint = request.url.path
    action = "UNKNOWN"

    if endpoint.startswith("/item"):
        if method == "POST":
            action = "ADD_INVENTORY"
        elif method == "GET":
            action = "LIST_INVENTORY" if endpoint == "/items" else "GET_INVENTORY"
        elif method == "PUT":
            action = "EDIT_INVENTORY"
        elif method == "DELETE":
            action = "DELETE_INVENTORY"

    #Build the JSON document to log to MongoDB
    log_document = {
        "timestamp": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": method,
        "endpoint": endpoint,
        "action": action,
        "user_agent": request.headers.get("user-agent", "Unknown")
    }

    # Save it to MongoDB 
    try:
         if not endpoint.startswith("/docs") and not endpoint.startswith("/openapi") and endpoint not in ["/", "/logs"] and method != "OPTIONS":
            await logs_collection.insert_one(log_document)
            print(f"Logged to Mongo: {log_document}") 
    except Exception as e:
        print(f"Failed to log to MongoDB: {e}")

    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=FileResponse)
def serve_ui():
    return "index.html"

#Add a new item (POST /item)
@app.post("/item", response_model=bouncer.ItemResponse)
def create_item(product: bouncer.ItemCreate, db: Session = Depends(get_db)):
    
    db_item = table.Item(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    # Add it to the database and save the changes
    db.add(db_item)
    db.commit()
    db.refresh(db_item) 
    
    return db_item

#Get an item by ID (GET /item/{id})
@app.get("/item/{item_id}", response_model=bouncer.ItemResponse)
def read_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(table.Item).filter(table.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

#Update an item by ID (PUT /item/{id})
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

#Delete an item by ID (DELETE /item/{id})
@app.delete("/item/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(table.Item).filter(table.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    
    return {"message": "Item deleted successfully"} 


#LIST VIEW: Get all items (GET /items)
@app.get("/items", response_model=list[bouncer.ItemResponse])
def list_items(db: Session = Depends(get_db)):
    return db.query(table.Item).all()

#Get API logs from MongoDB (GET /logs)
@app.get("/logs")
async def get_api_logs(skip: int = 0, limit: int = 5):
    # Fetch the most recent logs
    logs = await logs_collection.find({}, {"_id": 0}).sort("timestamp", -1).skip(skip).to_list(length=limit)
    return logs
