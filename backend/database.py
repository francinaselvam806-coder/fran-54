import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "hyperlocal_gig_finder"

# Initialize client with a timeout to prevent hanging
client = AsyncIOMotorClient(
    MONGO_URL, 
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000
)
db = client[DB_NAME]

async def get_database():
    try:
        # Verify connection
        await client.admin.command('ping')
        return db
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        # If connection fails, we might want to raise a cleaner error for FastAPI
        raise RuntimeError(f"Could not connect to MongoDB: {str(e)}")
