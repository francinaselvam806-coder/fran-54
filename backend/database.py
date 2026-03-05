import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, OperationFailure
from fastapi import HTTPException

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
        # Verify connection with a short timeout
        await client.admin.command('ping')
        return db
    except Exception as e:
        error_msg = f"MongoDB connection failed: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=503,
            detail=f"Database connection error. Please check MONGO_URL. Error: {str(e)}"
        )
