import httpx
import asyncio

async def test_registration():
    url = "http://127.0.0.1:8000/auth/register"
    data = {
        "username": "testuser_debug",
        "email": "test_debug@example.com",
        "password": "password123",
        "is_provider": True,
        "address": "Kanthalloor",
        "phone": "7012402897",
        "profile_image": None,
        "location": None
    }
    
    print(f"Calling: {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            print("Status Code:", response.status_code)
            print("Response:", response.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_registration())
