#!/usr/bin/env python3
"""
Test script for the new monitoring endpoints
"""

import requests
import json
import time

def test_monitoring_endpoints():
    """Test the monitoring endpoints"""
    base_url = "http://localhost:54338"  # Adjust port as needed
    
    print("🧪 Testing Monitoring Endpoints")
    print("=" * 50)
    
    # Test 1: Health check (public endpoint)
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/monitoring/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Generate token with valid marketing code
    print("\n2. Testing token generation...")
    try:
        # Use the current marketing code (you'll need to get this from the server output)
        marketing_code = "DREAM734$"  # Replace with actual current code
        
        response = requests.post(f"{base_url}/monitoring/token", data={
            'auth_code': marketing_code,
            'duration_minutes': 30
        })
        print(f"   Status: {response.status_code}")
        token_data = response.json()
        print(f"   Response: {json.dumps(token_data, indent=2)}")
        
        if token_data.get('success') and 'token' in token_data:
            token = token_data['token']
            print(f"   ✅ Token generated successfully!")
            
            # Test 3: Use token to access monitoring stats
            print("\n3. Testing monitoring stats with token...")
            try:
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(f"{base_url}/monitoring/stats", headers=headers)
                print(f"   Status: {response.status_code}")
                stats_data = response.json()
                print(f"   Response: {json.dumps(stats_data, indent=2)}")
                
                if stats_data.get('success'):
                    print("   ✅ Monitoring stats retrieved successfully!")
                else:
                    print("   ❌ Failed to retrieve monitoring stats")
                    
            except Exception as e:
                print(f"   Error: {e}")
        else:
            print("   ❌ Failed to generate token")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Try accessing stats without token (should fail)
    print("\n4. Testing unauthorized access...")
    try:
        response = requests.get(f"{base_url}/monitoring/stats")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("   ✅ Unauthorized access properly blocked!")
        else:
            print("   ❌ Security issue: unauthorized access allowed")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Try generating token with invalid code (should fail)
    print("\n5. Testing invalid marketing code...")
    try:
        response = requests.post(f"{base_url}/monitoring/token", data={
            'auth_code': 'INVALID123',
            'duration_minutes': 30
        })
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 403:
            print("   ✅ Invalid code properly rejected!")
        else:
            print("   ❌ Security issue: invalid code accepted")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")

if __name__ == "__main__":
    test_monitoring_endpoints()
