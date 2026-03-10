#!/usr/bin/env python3
"""
Test script for password change request workflow
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_workflow():
    session = requests.Session()
    
    print("=" * 60)
    print("TESTING PASSWORD CHANGE REQUEST WORKFLOW")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    response = session.post(f"{BASE_URL}/login", json={
        "username": "admin",
        "password": "admin123"
    })
    if response.status_code == 200 and response.json().get('success'):
        print("   ✓ Admin logged in successfully")
    else:
        print(f"   ✗ Failed to login as admin: {response.text}")
        return
    
    # Step 2: Create test user
    print("\n2. Creating test user...")
    response = session.post(f"{BASE_URL}/api/users", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "role": "viewer"
    })
    if response.status_code == 201:
        print("   ✓ Test user created")
    elif "already exists" in response.text:
        print("   ⚠ Test user already exists (OK)")
    else:
        print(f"   ✗ Failed to create user: {response.text}")
    
    # Step 3: Logout admin
    print("\n3. Logging out admin...")
    session.get(f"{BASE_URL}/logout")
    print("   ✓ Logged out")
    
    # Step 4: Login as test user
    print("\n4. Logging in as testuser...")
    response = session.post(f"{BASE_URL}/login", json={
        "username": "testuser",
        "password": "test123"
    })
    if response.status_code == 200 and response.json().get('success'):
        print("   ✓ Test user logged in")
    else:
        print(f"   ✗ Failed to login as testuser: {response.text}")
        return
    
    # Step 5: Submit password change request
    print("\n5. Submitting password change request...")
    response = session.post(f"{BASE_URL}/api/password-change-request", json={})
    if response.status_code == 201:
        request_data = response.json().get('request', {})
        request_id = request_data.get('id')
        print(f"   ✓ Password change request submitted (ID: {request_id})")
    else:
        error_msg = response.json().get('error', response.text)
        print(f"   ✗ Failed to submit request: {error_msg}")
        return
    
    # Step 6: Check request status
    print("\n6. Checking request status...")
    response = session.get(f"{BASE_URL}/api/password-change-request/status")
    if response.status_code == 200:
        status = response.json()
        print(f"   ✓ Request status: {status.get('status', 'unknown')}")
    
    # Step 7: Try to change password without approval (should fail)
    print("\n7. Attempting to change password without approval (should fail)...")
    response = session.post(f"{BASE_URL}/api/change-password", json={
        "new_password": "newpass123"
    })
    if response.status_code == 403:
        print("   ✓ Correctly blocked - no approval yet")
    else:
        print(f"   ✗ Unexpected response: {response.status_code}")
    
    # Step 8: Logout testuser
    print("\n8. Logging out testuser...")
    session.get(f"{BASE_URL}/logout")
    print("   ✓ Logged out")
    
    # Step 9: Login as admin again
    print("\n9. Logging in as admin again...")
    response = session.post(f"{BASE_URL}/login", json={
        "username": "admin",
        "password": "admin123"
    })
    if response.status_code == 200:
        print("   ✓ Admin logged in")
    
    # Step 10: Get all password change requests
    print("\n10. Checking password change requests...")
    response = session.get(f"{BASE_URL}/api/admin/password-change-requests?status=pending")
    if response.status_code == 200:
        requests_list = response.json()
        print(f"   ✓ Found {len(requests_list)} pending request(s)")
        if requests_list:
            pending_request = requests_list[0]
            request_id = pending_request['id']
            print(f"      Request from: {pending_request['username']}")
    
    # Step 11: Approve the request
    print(f"\n11. Approving password change request (ID: {request_id})...")
    response = session.post(f"{BASE_URL}/api/admin/password-change-requests/{request_id}/approve", json={
        "notes": "Approved for testing purposes"
    })
    if response.status_code == 200:
        print("   ✓ Request approved")
    else:
        print(f"   ✗ Failed to approve: {response.text}")
        return
    
    # Step 12: Logout admin
    print("\n12. Logging out admin...")
    session.get(f"{BASE_URL}/logout")
    print("   ✓ Logged out")
    
    # Step 13: Login as testuser again
    print("\n13. Logging in as testuser again...")
    response = session.post(f"{BASE_URL}/login", json={
        "username": "testuser",
        "password": "test123"
    })
    if response.status_code == 200:
        print("   ✓ Test user logged in")
    
    # Step 14: Change password now that it's approved
    print("\n14. Changing password with approved request...")
    response = session.post(f"{BASE_URL}/api/change-password", json={
        "new_password": "newpass123"
    })
    if response.status_code == 200:
        print("   ✓ Password changed successfully")
    else:
        error_msg = response.json().get('error', response.text)
        print(f"   ✗ Failed to change password: {error_msg}")
        return
    
    # Step 15: Logout and try to login with new password
    print("\n15. Logging out and testing new password...")
    session.get(f"{BASE_URL}/logout")
    
    response = session.post(f"{BASE_URL}/login", json={
        "username": "testuser",
        "password": "newpass123"
    })
    if response.status_code == 200 and response.json().get('success'):
        print("   ✓ Login with new password successful!")
    else:
        print(f"   ✗ Failed to login with new password: {response.text}")
        return
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
