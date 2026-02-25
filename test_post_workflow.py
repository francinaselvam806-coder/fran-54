import requests
import json

# Configuration
API_URL = "http://127.0.0.1:8000/services/"

# Test Data mimicking Student Workflow
payload = {
    "provider_email": "student_tutor@example.com",
    "title": "High School Math Tutor",
    "category": "Tutoring",
    "description": "I teach Algebra and Calculus to high school students.",
    "price": 20.0,
    "address": "Downtown Library",
    "skills": ["Math", "Algebra", "Calculus", "Teaching"]
}

try:
    print(f"Posting Service: {payload['title']}...")
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Service Posted Successfully!")
        print(f"Service ID: {data.get('_id')}")
        print(f"Certificate: {data.get('certificate')}")
        
        if data.get('certificate') and "Verified" in data.get('certificate'):
             print("\nSUCCESS: Auto-Certificate generation verified.")
        else:
             print("\nWARNING: Certificate missing or invalid.")
    else:
        print(f"\n❌ Failed to post service. Status: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"\n❌ Error: {e}")
