import asyncio
import motor.motor_asyncio
from backend.database import get_database
from backend.ai_engine import recommend_services

async def main():
    print("--- DB Check ---")
    db = await get_database()
    colls = await db.list_collection_names()
    print(f"Collections: {colls}")
    
    if "services" in colls:
        services = await db["services"].find({}).to_list(100)
        print(f"Services count: {len(services)}")
        for s in services:
            print(f"FULL Service Check: {s}")
    else:
        print("Collection 'services' not found!")

    print("\n--- AI Logic Check ---")
    query = "math tutor"
    print(f"Query: {query}")
    results = await recommend_services(query)
    print(f"Results found: {len(results)}")
    for r in results:
        print(f"- {r.get('title')} (Score: {r.get('ai_score')})")

if __name__ == "__main__":
    asyncio.run(main())
