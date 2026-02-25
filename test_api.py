import requests
import json

try:
    # Test Root
    print("Testing Root URL (http://127.0.0.1:8000/)...")
    r = requests.get("http://127.0.0.1:8000/")
    print(f"Root Status: {r.status_code}")
    print(f"Root Response: {r.text}")

    # Test Docs (should exist)
    print("\nTesting Docs (http://127.0.0.1:8000/docs)...")
    r = requests.get("http://127.0.0.1:8000/docs")
    print(f"Docs Status: {r.status_code}")

    # Test Services (should exist)
    print("\nTesting Services (http://127.0.0.1:8000/services/search?query=test)...")
    r = requests.get("http://127.0.0.1:8000/services/search?query=test")
    print(f"Services Status: {r.status_code}")

    # Test AI
    print("\nTesting AI Endpoint (http://127.0.0.1:8000/ai/recommend)...")
    payload = {"message": "web design"}
    r = requests.post("http://127.0.0.1:8000/ai/recommend", json=payload)
    print(f"AI Status: {r.status_code}")
    print(f"AI Response: {r.text}")
    
    # Test AI with Slash
    print("\nTesting AI Endpoint Slash (http://127.0.0.1:8000/ai/recommend/)...")
    r = requests.post("http://127.0.0.1:8000/ai/recommend/", json=payload)
    print(f"AI Slash Status: {r.status_code}")

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
