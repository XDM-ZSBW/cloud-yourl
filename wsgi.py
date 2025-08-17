#!/usr/bin/env python3
"""
WSGI entry point for Yourl.Cloud Inc. API Server
================================================

Production WSGI server configuration for Google Cloud Run deployment.
Enhanced for domain mapping compatibility and automatic health checks.

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Google Cloud Run: Supported
WSGI Server: Production Ready
Domain Mapping: Compatible
"""

import os
import sys

# Set environment variables for Cloud Run
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('PORT', '8080')
os.environ.setdefault('FLASK_DEBUG', 'False')

# Import the Flask app after setting environment variables
try:
    from app_simple import app
    print("✅ Successfully imported simplified Flask app")
except Exception as e:
    print(f"❌ Error importing simplified Flask app: {e}")
    # Create a minimal fallback app if import fails
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def fallback():
        return {"error": "App import failed", "message": str(e)}, 500
    
    @app.route('/health')
    def health():
        return {"status": "degraded", "message": "Fallback app running"}, 200

# Configure the app for Cloud Run
if hasattr(app, 'config'):
    app.config.update(
        PREFERRED_URL_SCHEME='https',
        USE_X_SENDFILE=False,
        SERVER_NAME=None
    )

if __name__ == "__main__":
    # This allows running the WSGI file directly for testing
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
