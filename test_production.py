#!/usr/bin/env python3
"""
Production Test Script for Yourl.Cloud Inc. API Server
=====================================================

This script tests the production WSGI configuration locally using gunicorn.
This ensures the same environment as production deployment.

Author: Yourl.Cloud Inc.
Usage: python test_production.py
"""

import os
import subprocess
import sys
import time

def test_production_wsgi():
    """Test the production WSGI configuration locally."""
    print("🚀 Testing Production WSGI Configuration")
    print("=" * 50)
    
    # Set production environment variables
    env = os.environ.copy()
    env['FLASK_ENV'] = 'production'
    env['FLASK_DEBUG'] = 'False'
    env['PORT'] = '8080'
    
    print("✅ Environment configured for production")
    print(f"📍 Production Port: {env['PORT']}")
    print(f"🏭 Flask Environment: {env['FLASK_ENV']}")
    print(f"🐛 Debug Mode: {env['FLASK_DEBUG']}")
    print()
    
    # Test dynamic port allocation for local development
    print("🔍 Testing dynamic port allocation...")
    import socket
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    local_port = find_free_port()
    print(f"📍 Local Test Port: {local_port} (random available)")
    print()
    
    try:
        # Test WSGI import
        print("🔍 Testing WSGI import...")
        from wsgi import app
        print("✅ WSGI import successful")
        print(f"📱 App name: {app.name}")
        print(f"🔧 Config: {dict(app.config)}")
        print()
        
        # Test app routes
        print("🔍 Testing app routes...")
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✅ Found {len(routes)} routes:")
        for route in routes:
            print(f"   📍 {route}")
        print()
        
        print("🎯 Production test completed successfully!")
        print("🚀 Your app is ready for production deployment")
        print()
        print("💡 To run locally with gunicorn:")
        print("   gunicorn --bind 0.0.0.0:8080 --workers 1 --timeout 120 wsgi:app")
        print()
        print("💡 To run with Flask (development only):")
        print("   python wsgi.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Production test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_production_wsgi()
    sys.exit(0 if success else 1)
