import asyncio
from backend.ai_engine import recommend_services
import sys

# Windows Fix
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

async def test_web_design():
    query = "i need web design"
    print(f"Testing Query: '{query}'")
    
    try:
        results = await recommend_services(query)
        
        print(f"\nFound {len(results)} matches:")
        for r in results:
            print(f"✅ Service: {r.get('title')} | Category: {r.get('category')} | Score: {r.get('ai_score')}")
            
        # success check
        has_web_design = any("web" in r.get('title').lower() for r in results)
        if has_web_design:
            print("\nSUCCESS: AI successfully found the web design service!")
        else:
            print("\nFAILURE: AI did NOT find the web design service.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_web_design())
