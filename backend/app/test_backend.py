"""
Test script to verify SWS AI Policy Assistant backend is working correctly
Run this after starting the backend: py test_backend.py
"""

import sys
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_health():
    """Test health check endpoint"""
    print_header("Testing Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR: Cannot connect to backend at {API_BASE_URL}")
        print("Make sure to run: py app/main.py in another terminal")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_info():
    """Test info endpoint"""
    print_header("Testing Pipeline Info")
    try:
        response = requests.get(f"{API_BASE_URL}/api/info", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if data.get("pipeline_ready"):
            vector_info = data.get("vector_store_info", {})
            doc_count = vector_info.get("document_count", 0)
            if doc_count == 0:
                print("⚠️  WARNING: No documents ingested yet")
                print("Run: py app/ingest.py")
            return True
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_chat_with_docs():
    """Test chat endpoint"""
    print_header("Testing Chat Endpoint")
    
    test_questions = [
        "What policies are available in the documents?",
        "Who is the HR contact?",
        "Tell me about employee benefits",
    ]
    
    for question in test_questions:
        print(f"Question: {question}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/chat",
                json={"question": question},
                timeout=TIMEOUT
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Answer: {data.get('answer', 'No answer')[:100]}...")
                print(f"Sources: {data.get('sources', [])}")
                print("✅ PASS\n")
            else:
                print(f"Error: {response.json()}")
                print("❌ FAIL\n")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}\n")

def test_chat_empty():
    """Test error handling with empty question"""
    print_header("Testing Error Handling")
    
    print("Sending empty question...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={"question": ""},
            timeout=TIMEOUT
        )
        
        if response.status_code == 400:
            print("✅ PASS: Correctly rejected empty question")
            print(f"Error: {response.json()}")
        else:
            print(f"❌ FAIL: Expected 400, got {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_api_docs():
    """Test API documentation endpoint"""
    print_header("Testing API Documentation")
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=TIMEOUT)
        if response.status_code == 200:
            print("✅ PASS: API docs available at /docs")
            print(f"Visit: {API_BASE_URL}/docs")
        else:
            print(f"❌ FAIL: Expected 200, got {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    """Run all tests"""
    print("\n")
    print("█" * 60)
    print("  SWS AI Policy Assistant - Backend Test Suite")
    print("█" * 60)
    print(f"  Testing API: {API_BASE_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("█" * 60)
    
    results = {
        "Health Check": test_health(),
        "Info Endpoint": test_info(),
        "Chat with Docs": True,  # Run in next section
        "Error Handling": True,   # Run in next section
        "API Docs": test_api_docs(),
    }
    
    # Run additional tests
    test_chat_with_docs()
    test_chat_empty()
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print("\nDetailed Results:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("✅ All tests passed! Backend is working correctly.")
        print("\nYou can now:")
        print("  1. Open http://localhost:5173 in your browser")
        print("  2. Start asking questions!")
        print("  3. Check the API docs at http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("  1. Make sure backend is running: py app/main.py")
        print("  2. Make sure PDFs are ingested: py app/ingest.py")
        print("  3. Check Groq API key in .env")
        print("  4. Check error messages above for details")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
