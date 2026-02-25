import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    mongo_url = "mongodb://localhost:27017"
    client = AsyncIOMotorClient(mongo_url)
    
    print("Connecting to MongoDB at:", mongo_url)
    
    try:
        # List all database names
        dbs = await client.list_database_names()
        print("Databases found:", dbs)
        
        target_db = "hyperlocal_gig_finder"
        if target_db in dbs:
            print(f"\nSUCCESS: Database '{target_db}' exists.")
            db = client[target_db]
            collections = await db.list_collection_names()
            print("Collections:", collections)
            
            for col_name in collections:
                count = await db[col_name].count_documents({})
                print(f" - {col_name}: {count} documents")
                if count > 0:
                    doc = await db[col_name].find_one()
                    print(f"   Sample doc: {doc}")
        else:
            print(f"\nWARNING: Database '{target_db}' NOT found in the list.")
            
    except Exception as e:
        print("Error connecting or listing databases:", e)

if __name__ == "__main__":
    asyncio.run(main())
