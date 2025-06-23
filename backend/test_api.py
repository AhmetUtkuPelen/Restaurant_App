"""
Simple test script to demonstrate the Chat API functionality
Run this after starting the FastAPI server with: uvicorn main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_registration():
    """Test user registration"""
    print("=== Testing User Registration ===")
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "display_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_user_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    
    login_data = {
        "username_or_email": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_get_users():
    """Test getting all users"""
    print("\n=== Testing Get All Users ===")
    
    response = requests.get(f"{BASE_URL}/users/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_create_message():
    """Test creating a message"""
    print("\n=== Testing Create Message ===")
    
    message_data = {
        "recipient_id": "test_recipient_id",
        "content": "Hello, this is a test message!",
        "message_type": "text"
    }
    
    response = requests.post(f"{BASE_URL}/messages/", json=message_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_search_users():
    """Test user search"""
    print("\n=== Testing User Search ===")
    
    response = requests.get(f"{BASE_URL}/users/search/?q=test")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    """Run all tests"""
    print("Starting Chat API Tests...")
    print("Make sure the server is running on http://localhost:8000")
    
    try:
        # Test basic endpoint
        response = requests.get(f"{BASE_URL}/")
        print(f"Server status: {response.status_code}")
        print(f"Server response: {response.json()}")
        
        # Run tests
        user = test_user_registration()
        test_user_login()
        test_get_users()
        test_search_users()
        message = test_create_message()
        
        print("\n=== All tests completed! ===")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure to start the server with: uvicorn main:app --reload")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
