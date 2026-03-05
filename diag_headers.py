import httpx
import asyncio

async def diagnose_headers():
    url = "https://fran-54.onrender.com/auth/register"
    data = {
        "username": "diag_test",
        "email": "diag@example.com",
        "password": "password123",
        "is_provider": False,
        "address": "test",
        "phone": "0000000000",
        "profile_image": None,
        "location": None
    }
    
    print(f"Diagnosing: {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            print("\n--- RESPONSE INFO ---")
            print(f"Status Code: {response.status_code}")
            print("\n--- HEADERS ---")
            for key, val in response.headers.items():
                print(f"{key}: {val}")
            print("\n--- CONTENT ---")
            print(response.text)
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    asyncio.run(diagnose_headers())
