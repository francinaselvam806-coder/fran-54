import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    mongo_url = "mongodb://localhost:27017"
    client = AsyncIOMotorClient(mongo_url)
    db_name = "hyperlocal_gig_finder"
    
    print(f"Attempting to write to {db_name} on {mongo_url}...")
    
    try:
        db = client[db_name]
        # Insert a test document
        result = await db["test_collection"].insert_one({"test": "data", "status": "checking write access"})
        print(f"Successfully inserted document with ID: {result.inserted_id}")
        
        # Check if DB exists now
        dbs = await client.list_database_names()
        if db_name in dbs:
            print(f"SUCCESS: Database '{db_name}' now appears in the list.")
            print("Please refreshing MongoDB Compass now.")
        else:
            print(f"WARNING: Database '{db_name}' still NOT in list (might be delayed).")

    except Exception as e:
        print("FAILED to write to database:", e)

if __name__ == "__main__":
    asyncio.run(main())
