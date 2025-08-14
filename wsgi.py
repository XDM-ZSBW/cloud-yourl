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
from app import app, CLOUD_RUN_CONFIG

# Configure environment for Cloud Run domain mapping
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('PORT', '8080')

# Ensure the app is configured for Cloud Run
if __name__ == "__main__":
    # This allows running the WSGI file directly for testing
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
