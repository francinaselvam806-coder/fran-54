import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "hyperlocal_gig_finder")

async def revoke_admin_access():
    print(f"Connecting to MongoDB at {MONGO_URL} (DB: {DB_NAME})...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    email = input("Enter the email of the user to REMOVE ADMIN rights from: ").strip()
    
    if not email:
        print("Error: Email cannot be empty.")
        return

    # Find User
    user = await db["users"].find_one({"email": email})
    
    if not user:
        print(f"❌ User '{email}' not found.")
        return

    # Update User
    result = await db["users"].update_one(
        {"email": email},
        {"$set": {"is_admin": False}}
    )
    
    if result.modified_count > 0:
        print(f"✅ SUCCESS: User '{user.get('username')}' is NO LONGER an Admin.")
    else:
        if not user.get("is_admin"):
             print(f"ℹ️  User '{email}' was not an admin to begin with.")
        else:
             print("❌ Failed to update user.")

    client.close()

if __name__ == "__main__":
    asyncio.run(revoke_admin_access())
