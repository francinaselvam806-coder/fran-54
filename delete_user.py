import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "hyperlocal_gig_finder")

async def delete_user():
    print(f"Connecting to MongoDB at {MONGO_URL} (DB: {DB_NAME})...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    email = input("Enter the email of the user to PERMANENTLY DELETE: ").strip()
    
    if not email:
        print("Error: Email cannot be empty.")
        return

    # Find User
    user = await db["users"].find_one({"email": email})
    
    if not user:
        print(f"❌ User '{email}' not found.")
        return

    # Confirm
    confirm = input(f"⚠️  Are you sure you want to DELETE user '{user.get('username')}'? (yes/no): ").lower()
    if confirm != "yes":
        print("Operation cancelled.")
        return

    # Delete User
    result = await db["users"].delete_one({"email": email})
    
    if result.deleted_count > 0:
        print(f"✅ SUCCESS: User '{email}' has been deleted from the database.")
    else:
        print("❌ Failed to delete user.")

    client.close()

if __name__ == "__main__":
    asyncio.run(delete_user())
