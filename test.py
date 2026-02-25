import asyncio
import os
import sys

# Ensure backend path is reachable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from backend.database import get_database
from backend.ai_engine import recommend_services

async def main():
    print("---------------------------------------------------------")
    print("      AI Model Test Script - Service Recommendation      ")
    print("---------------------------------------------------------")
    print("Connecting to Database...")
    
    try:
        db = await get_database()
        # Verify connection by listing collections
        colls = await db.list_collection_names()
        print(f"Connected! Collections found: {len(colls)}")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    print("\nSystem ready. Enter a query to find services.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_query = input("User Input (Search/Requirement): ").strip()
            
            if user_query.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            
            if not user_query:
                continue

            print(f"Analyzing query: '{user_query}'...")
            recommendations = await recommend_services(user_query)
            
            if recommendations:
                print(f"\nFound {len(recommendations)} recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    title = rec.get('title', 'No Title')
                    score = rec.get('ai_score', 0)
                    skills = ", ".join(rec.get('skills', []))
                    print(f"{i}. {title} (Match Score: {score})")
                    print(f"   Skills: {skills}\n")
            else:
                print("No matching services found. Try different keywords.\n")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Windows SelectorEventLoop policy fix if needed, though usually for 3.8+
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
