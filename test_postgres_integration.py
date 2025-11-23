#!/usr/bin/env python3
"""
Test script to verify PostgreSQL integration works correctly
Run this after starting the backend to validate setup
"""

import requests
import json
import tempfile
import csv
from pathlib import Path
import time

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}→ {text}{Colors.RESET}")

def create_test_csv():
    """Create a simple test CSV file"""
    fd, path = tempfile.mkstemp(suffix='.csv')
    try:
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'sales', 'month'])
            writer.writerow([1, 'Product A', 100, 'Jan'])
            writer.writerow([2, 'Product B', 200, 'Feb'])
            writer.writerow([3, 'Product A', 150, 'Mar'])
            writer.writerow([4, 'Product B', 250, 'Apr'])
            writer.writerow([5, 'Product A', 180, 'May'])
        return path
    finally:
        import os
        os.close(fd)

def test_backend_health():
    """Test if backend is running"""
    print_info("Testing backend connection...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Backend is running")
            data = response.json()
            print(f"  Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cannot connect to backend: {e}")
        return False

def test_upload_csv():
    """Test CSV upload and verify it's saved to PostgreSQL"""
    print_info("Uploading test CSV file...")
    csv_path = create_test_csv()
    
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': (Path(csv_path).name, f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print_success("CSV uploaded successfully")
            print(f"  Session ID: {data['session_id']}")
            print(f"  Rows: {data['rows']}")
            print(f"  Columns: {', '.join(data['columns'])}")
            print(f"  Storage: {data['storage']}")
            return data['session_id']
        else:
            print_error(f"Upload failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    finally:
        import os
        os.remove(csv_path)

def test_query(session_id):
    """Test querying the CSV"""
    print_info("Querying CSV data...")
    
    query = "What is the mean of the sales column?"
    payload = {
        "session_id": session_id,
        "query": query
    }
    
    try:
        response = requests.post(f"{BASE_URL}/query", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Query processed successfully")
            print(f"  Query: {data['query']}")
            print(f"  Response: {data['response'][:100]}...")
            print(f"  Storage: {data['storage']}")
            return True
        else:
            print_error(f"Query failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Query error: {e}")
        return False

def test_get_messages(session_id):
    """Test retrieving chat messages from PostgreSQL"""
    print_info("Retrieving chat messages from database...")
    
    try:
        response = requests.get(f"{BASE_URL}/session/{session_id}/messages")
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            print_success(f"Retrieved {len(messages)} messages from PostgreSQL")
            for i, msg in enumerate(messages):
                msg_type = f"[{msg['message_type'].upper()}]"
                content = msg['content'][:50]
                print(f"  {i+1}. {msg_type} {content}...")
            return True
        else:
            print_error(f"Failed to get messages: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error retrieving messages: {e}")
        return False

def test_list_sessions():
    """Test listing all sessions"""
    print_info("Listing all sessions...")
    
    try:
        response = requests.get(f"{BASE_URL}/sessions")
        
        if response.status_code == 200:
            data = response.json()
            sessions = data.get('sessions', [])
            print_success(f"Found {len(sessions)} session(s)")
            for session in sessions:
                print(f"  - {session['filename']}: {session['message_count']} messages, {session['metadata']['rows']} rows")
            return True
        else:
            print_error(f"Failed to list sessions: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error listing sessions: {e}")
        return False

def test_session_info(session_id):
    """Test getting session info"""
    print_info("Getting session information...")
    
    try:
        response = requests.get(f"{BASE_URL}/session/{session_id}/info")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Session info retrieved")
            print(f"  Filename: {data['filename']}")
            print(f"  Rows: {data['rows']}")
            print(f"  Columns: {', '.join(data['columns'])}")
            print(f"  Messages: {data['message_count']}")
            print(f"  Storage: {data['storage']}")
            return True
        else:
            print_error(f"Failed to get session info: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting session info: {e}")
        return False

def test_persistence():
    """Test that data persists across requests"""
    print_info("Testing data persistence...")
    
    # Upload a CSV
    csv_path = create_test_csv()
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': ('test.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code != 200:
            print_error("Failed to upload for persistence test")
            return False
        
        session_id = response.json()['session_id']
        
        # Ask a question
        payload = {
            "session_id": session_id,
            "query": "Show me the first 3 rows"
        }
        response = requests.post(f"{BASE_URL}/query", json=payload)
        
        if response.status_code != 200:
            print_error("Failed to query for persistence test")
            return False
        
        time.sleep(1)  # Wait a bit
        
        # Retrieve messages - this tests if they're really in PostgreSQL
        response = requests.get(f"{BASE_URL}/session/{session_id}/messages")
        
        if response.status_code == 200:
            messages = response.json()['messages']
            if len(messages) >= 2:  # User query + AI response
                print_success("Data persisted to PostgreSQL successfully!")
                return True
            else:
                print_error("Messages not persisted correctly")
                return False
        else:
            print_error("Failed to retrieve persisted messages")
            return False
    finally:
        import os
        os.remove(csv_path)

def main():
    print_header("PostgreSQL Integration Test Suite")
    print("Testing CSV Chatbot with PostgreSQL Backend\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Backend health
    tests_total += 1
    if test_backend_health():
        tests_passed += 1
    
    # Test 2: Upload CSV
    tests_total += 1
    session_id = test_upload_csv()
    if session_id:
        tests_passed += 1
    else:
        print_error("Cannot continue without session ID")
        print_header("Test Results")
        print_error(f"Tests passed: {tests_passed}/{tests_total}")
        return
    
    time.sleep(1)
    
    # Test 3: Query
    tests_total += 1
    if test_query(session_id):
        tests_passed += 1
    
    time.sleep(1)
    
    # Test 4: Get messages
    tests_total += 1
    if test_get_messages(session_id):
        tests_passed += 1
    
    # Test 5: Session info
    tests_total += 1
    if test_session_info(session_id):
        tests_passed += 1
    
    # Test 6: List sessions
    tests_total += 1
    if test_list_sessions():
        tests_passed += 1
    
    # Test 7: Persistence
    tests_total += 1
    if test_persistence():
        tests_passed += 1
    
    # Summary
    print_header("Test Results")
    total_tests = tests_passed
    if tests_passed == tests_total:
        print_success(f"All tests passed! ({tests_passed}/{tests_total})")
        print(f"\n{Colors.GREEN}PostgreSQL integration is working correctly!{Colors.RESET}")
    else:
        failed = tests_total - tests_passed
        print_error(f"{failed} test(s) failed ({tests_passed}/{tests_total} passed)")
        print(f"\n{Colors.RED}Please check the errors above.{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")

if __name__ == "__main__":
    main()
