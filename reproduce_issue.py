import requests
import json

BASE_URL = "http://localhost:8000/prescriptions"

def test_malformed():
    print("Testing Malformed Request (Missing Patient)...")
    # Missing 'patient'
    payload = {
        "clinic": {"id": 1},
        "physician": {"id": 1},
        "text": "Dipirona"
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_invalid_physician():
    print("\nTesting Invalid Physician...")
    payload = {
        "clinic": {"id": 1},
        "physician": {"id": 999}, # Invalid ID
        "patient": {"id": 1},
        "text": "Dipirona"
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_valid():
    print("\nTesting Valid Request...")
    payload = {
        "clinic": {"id": 1},
        "physician": {"id": 1},
        "patient": {"id": 1},
        "text": "Dipirona"
    }
    try:
        response = requests.post(BASE_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_malformed()
    test_invalid_physician()
    test_valid()
