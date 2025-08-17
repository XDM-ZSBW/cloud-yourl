#!/usr/bin/env python3
"""
Simple test script to verify the Flask app can start
"""

import os
import sys

# Set environment variables for testing
os.environ['FLASK_ENV'] = 'production'
os.environ['PORT'] = '8080'
os.environ['FLASK_DEBUG'] = 'False'

print("🧪 Testing Flask app import...")

try:
    # Test importing the simplified app
    from app_simple import app
    print("✅ Successfully imported app_simple")
    
    # Test importing the WSGI entry point
    from wsgi import app as wsgi_app
    print("✅ Successfully imported wsgi:app")
    
    # Test basic app functionality
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        print(f"✅ Health endpoint: {response.status_code}")
        
        # Test root endpoint
        response = client.get('/')
        print(f"✅ Root endpoint: {response.status_code}")
        
        # Test status endpoint
        response = client.get('/status')
        print(f"✅ Status endpoint: {response.status_code}")
    
    print("🎉 All tests passed! App is ready for deployment.")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
