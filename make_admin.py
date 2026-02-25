import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "hyperlocal_gig_finder")

async def promote_user_to_admin():
    # 1. Connect to Database
    print(f"Connecting to MongoDB at {MONGO_URL} (DB: {DB_NAME})...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # 2. Get User Email
    email = input("Enter the email of the user you want to make Admin: ").strip()
    
    if not email:
        print("Error: Email cannot be empty.")
        return

    # 3. Find User
    user = await db["users"].find_one({"email": email})
    
    if not user:
        print(f"❌ User with email '{email}' not found.")
        print("-" * 30)
        print("🔍 checking available users in database...")
        # List first 10 users to help debug
        cursor = db["users"].find({}, {"email": 1, "username": 1}).limit(10)
        users = await cursor.to_list(length=10)
        
        if not users:
            print("⚠️  No users found in the database at all!")
            print("   Please go to the website registration page and create an account first.")
        else:
            print("Found these users (check for typos):")
            for u in users:
                print(f" - {u.get('email', 'No Email')} ({u.get('username', 'No Name')})")
        print("-" * 30)
        return

    # 4. Update User
    result = await db["users"].update_one(
        {"email": email},
        {"$set": {"is_admin": True}}
    )
    
    if result.modified_count > 0:
        print(f"✅ SUCCESS: User '{user['username']}' ({email}) is now an Admin!")
        print("You can now log in and access the Admin Dashboard.")
    else:
        if user.get("is_admin"):
            print(f"ℹ️  User '{email}' is ALREADY an admin.")
        else:
            print("❌ Failed to update user. Unknown error.")

    client.close()

if __name__ == "__main__":
    asyncio.run(promote_user_to_admin())
