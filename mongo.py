from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://lili:lilian17@inventory_mongo:27017/"

#Connect to the MongoDB server
client = AsyncIOMotorClient(MONGO_URL)

#Create a database called "inventory_logs_db"
db = client["inventory_logs_db"]

logs_collection = db["api_logs"]