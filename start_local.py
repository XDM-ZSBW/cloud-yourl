#!/usr/bin/env python3
"""
Local Development Server for Yourl.Cloud Inc. API Server
========================================================

This script starts the Flask app locally without development server warnings.
It uses a production-like configuration for local testing.

Author: Yourl.Cloud Inc.
Usage: python start_local.py
"""

import os
import sys
import socket
import time

def find_free_port():
    """Find a random available port for local testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """Start the Flask app locally with production configuration."""
    print("🚀 Starting Yourl.Cloud API Server (Local Development)")
    print("=" * 60)
    
    # Set production environment variables (removed problematic WERKZEUG_RUN_MAIN)
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = 'False'
    
    # Find a random available port
    local_port = find_free_port()
    
    print(f"📍 Port: {local_port}")
    print(f"🏭 Environment: Production")
    print(f"🐛 Debug: False")
    print(f"☁️ Cloud Run Support: Enabled")
    print("=" * 60)
    print("⚠️  NOTE: This is for local testing only!")
    print("🚀 For production, use: gunicorn --bind 0.0.0.0:8080 wsgi:app")
    print("=" * 60)
    
    try:
        # Import the WSGI app
        from wsgi import app
        
        # Configure for production
        app.config.update(
            PREFERRED_URL_SCHEME='https',
            USE_X_SENDFILE=False,
            SERVER_NAME=None,
            TESTING=False,
            DEBUG=False,
            ENV='production'
        )
        
        # Track start time for uptime monitoring (using module-level variable)
        global _app_start_time
        if '_app_start_time' not in globals():
            _app_start_time = time.time()
        
        print(f"✅ App configured for production")
        print(f"🌐 Server starting on http://localhost:{local_port}")
        print(f"⏰ Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Start the server with production settings
        app.run(
            host='0.0.0.0',
            port=local_port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
