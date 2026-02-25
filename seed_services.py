import asyncio
import random
from motor.motor_asyncio import AsyncIOMotorClient

# Database Config
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "hyperlocal_gig_finder"

# Sample Data
services_data = [
    {
        "title": "Professional Plumbing Service",
        "category": "Home Service",
        "skills": ["plumbing", "pipe repair", "leak fix", "installation"],
        "description": "Expert plumber for all your home repair needs. Fixing leaks, installing taps, and more.",
        "price": 50,
        "provider_id": "user_001",
        "provider_email": "plumber@example.com"
    },
    {
        "title": "Expert Math Tutor",
        "category": "Education",
        "skills": ["math", "algebra", "calculus", "tutor", "teaching"],
        "description": "Experienced math tutor for high school and college students. simplify complex concepts.",
        "price": 30,
        "provider_id": "user_002",
        "provider_email": "tutor@example.com"
    },
    {
        "title": "Full Stack Web Developer",
        "category": "IT & Tech",
        "skills": ["web development", "javascript", "react", "python", "node.js", "html", "css"],
        "description": "Building modern, responsive websites and web applications using the latest technologies.",
        "price": 80,
        "provider_id": "user_003",
        "provider_email": "dev@example.com"
    },
    {
        "title": "Graphic Design & Logo Creation",
        "category": "Design",
        "skills": ["graphic design", "logo", "photoshop", "illustrator", "branding"],
        "description": "Creative graphic designer for logos, brochures, and brand identity materials.",
        "price": 45,
        "provider_id": "user_004",
        "provider_email": "designer@example.com"
    },
    {
        "title": "Certified Yoga Instructor",
        "category": "Health",
        "skills": ["yoga", "fitness", "meditation", "wellness", "health"],
        "description": "Private yoga sessions to improve flexibility, strength, and mental peace.",
        "price": 40,
        "provider_id": "user_005",
        "provider_email": "yoga@example.com"
    },
    {
        "title": "Wedding Photographer",
        "category": "Events",
        "skills": ["photography", "wedding", "events", "camera", "editing"],
        "description": "Capturing your special moments with professional wedding photography services.",
        "price": 150,
        "provider_id": "user_006",
        "provider_email": "photo@example.com"
    },
    {
        "title": "Electrician - Wiring & Repairs",
        "category": "Home Service",
        "skills": ["electrician", "wiring", "repair", "lighting", "circuit"],
        "description": "Licensed electrician for safe and reliable electrical repairs and installations.",
        "price": 60,
        "provider_id": "user_007",
        "provider_email": "electric@example.com"
    },
    {
        "title": "English Language Coach",
        "category": "Education",
        "skills": ["english", "teaching", "grammar", "speaking", "language"],
        "description": "Improve your English speaking and writing skills with personalized coaching.",
        "price": 25,
        "provider_id": "user_008",
        "provider_email": "english@example.com"
    },
    {
        "title": "Python Scripting & Automation",
        "category": "IT & Tech",
        "skills": ["python", "scripting", "automation", "coding", "data"],
        "description": "Automate boring tasks and process data efficiently with custom Python scripts.",
        "price": 55,
        "provider_id": "user_009",
        "provider_email": "pydev@example.com"
    }
]

async def seed_db():
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["services"]

    print("Clearing existing services...")
    await collection.delete_many({})

    print(f"Seeding {len(services_data)} services...")
    result = await collection.insert_many(services_data)
    
    print(f"Successfully inserted {len(result.inserted_ids)} documents.")
    print("Done!")

if __name__ == "__main__":
    asyncio.run(seed_db())
