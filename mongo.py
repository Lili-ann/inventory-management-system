from motor.motor_asyncio import AsyncIOMotorClient

# The connection string to your Dockerized MongoDB
# Note: 27017 is the default port. If you changed it in your docker-compose.yml, update it here!
MONGO_URL = "mongodb://lili:lilian17@localhost:27017/"

# 1. Connect to the MongoDB server
client = AsyncIOMotorClient(MONGO_URL)

# 2. Create or connect to a database (Mongo creates it automatically if it doesn't exist)
db = client["inventory_logs_db"]

# 3. Create or connect to the specific collection requested in your rubric
logs_collection = db["api_logs"]