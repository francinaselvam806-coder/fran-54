import os
from motor.motor_asyncio import AsyncIOMotorClient

# Default to local MongoDB if not specified
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "hyperlocal_gig_finder"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

async def get_database():
    return db
