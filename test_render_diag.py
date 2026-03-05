import httpx
import asyncio
import time

async def test_render_registration():
    # Use the live Render URL
    url = "https://fran-54.onrender.com/auth/register"
    
    # Unique username to avoid "Email already registered" error
    timestamp = int(time.time())
    data = {
        "username": f"test_user_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "password123",
        "is_provider": False,
        "address": "Diagnostic Test",
        "phone": "0000000000",
        "profile_image": None,
        "location": None
    }
    
    print(f"--- DIAGNOSTIC TEST ---")
    print(f"Target URL: {url}")
    print(f"Test Email: {data['email']}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=data)
            
            print(f"Status Code: {response.status_code}")
            
            try:
                json_data = response.json()
                print("Response JSON:", json_data)
                
                if response.status_code == 201:
                    print("\n✅ SUCCESS: Registration works on Render!")
                elif response.status_code == 503:
                    print("\n❌ DATABASE ERROR: The backend is running but cannot reach MongoDB.")
                    print(f"Reason: {json_data.get('detail')}")
                else:
                    print("\n⚠️ API returned an error.")
                    print(f"Reason: {json_data.get('detail')}")
            except Exception:
                print("Response is NOT JSON. Raw content:")
                print(response.text)
                print("\n❌ CRITICAL: Backend is crashed or misconfigured (returned HTML).")
                
    except Exception as e:
        print(f"\n❌ NETWORK ERROR: Could not reach Render server.")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_render_registration())
