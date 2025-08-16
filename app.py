#!/usr/bin/env python3
"""
Simple API Server with Visual Inspection and Google Cloud Run Support
====================================================================

A self-executing Python Flask application that responds with the request URL
and provides visual inspection capabilities for PC and phone devices.
Enhanced for Google Cloud Run deployment with dual-mode endpoint support.
Production-ready with WSGI server support.

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Friends and Family Guard: Enabled
Google Cloud Run: Supported
WSGI Server: Production Ready
Domain Mapping: Compatible
"""

from flask import Flask, request, jsonify, render_template_string, render_template, make_response, session, Response, redirect
import socket
import os
import re
import logging
import platform
import subprocess
import sys
import webbrowser
import threading
import time
import hashlib
import random
from datetime import datetime
from urllib.parse import urlparse

# Configure logging for production cloud environments
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set a secret key for Flask sessions (required for session management)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'yourl-cloud-secret-key-2024')

# Configuration - Google Cloud Run compatible with domain mapping support
HOST = '0.0.0.0'  # Listen on all interfaces (required for Cloud Run)

# Port configuration - Use random available port for local development, 8080 for production
if os.environ.get('PORT'):
    # Production environment (Cloud Run) - use environment PORT
    PORT = int(os.environ.get('PORT', 8080))
else:
    # Local development - use random available port
    import socket
    def find_free_port():
        """Find a free port to use for local development"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to any available port
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    PORT = find_free_port()

DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
# Production mode detection - All instances deploy as production instances
PRODUCTION = True  # Always production for all deployments

# Cloud Run Domain Mapping Configuration
# These settings ensure compatibility with custom domain mappings
CLOUD_RUN_CONFIG = {
    "domain_mapping_enabled": True,
    "region": "us-west1",  # Default region for domain mappings
    "trust_proxy": True,  # Trust X-Forwarded headers from Cloud Run proxy
    "cors_enabled": True,  # Enable CORS for domain mapping compatibility
    "health_check_path": "/health",  # Health check endpoint for Cloud Run
    "readiness_check_path": "/health"  # Readiness check endpoint
}

# Add module-level cache for generated codes
_generated_code_cache = None
_generated_hash_code_cache = {}

def generate_marketing_code():
    """
    Generate a fun, marketing-friendly password that changes with each commit.
    Uses git commit hash to ensure consistency within a commit but changes between commits.
    Only uses basic ASCII characters for maximum compatibility.
    """
    global _generated_code_cache
    
    # Return cached code if available
    if _generated_code_cache is not None:
        return _generated_code_cache
    
    try:
        # Get the current git commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                            text=True, stderr=subprocess.DEVNULL).strip()[:8]
    except:
        # Fallback if git is not available - use a stable identifier
        # Use environment variable or a fixed string to ensure consistency
        fallback_id = os.environ.get('BUILD_ID', os.environ.get('DEPLOYMENT_ID', 'stable-fallback'))
        commit_hash = hashlib.md5(fallback_id.encode()).hexdigest()[:8]
    
    # Fun marketing words and phrases (ASCII only)
    marketing_words = [
        "CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE", "LAUNCH", "FLY",
        "SPARK", "SHINE", "GLOW", "RISE", "LEAP", "JUMP", "DASH", "ZOOM",
        "POWER", "MAGIC", "WONDER", "AMAZE", "THRILL", "EXCITE", "INSPIRE", "IGNITE",
        "ROCKET", "STAR", "MOON", "SUN", "OCEAN", "MOUNTAIN", "FOREST", "RIVER",
        "TECH", "AI", "CODE", "DATA", "SMART", "FAST", "SECURE", "TRUST",
        "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "GANG", "TRIBE", "CLAN"
    ]
    
    # Fun ASCII symbols and characters
    ascii_symbols = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
    
    # Generate a deterministic but fun password using the commit hash
    # Convert commit hash to a number for seeding
    hash_num = int(commit_hash, 16)
    random.seed(hash_num)
    
    # Pick a random marketing word
    word = random.choice(marketing_words)
    
    # Pick a random ASCII symbol
    symbol = random.choice(ascii_symbols)
    
    # Generate a short number (2-3 digits)
    number = random.randint(10, 999)
    
    # Combine them in a fun way (ASCII only)
    password = f"{word}{number}{symbol}"
    
    # Cache the generated code
    _generated_code_cache = password
    
    return password

def generate_marketing_code_from_hash(commit_hash: str):
    """Generate marketing code from specific commit hash"""
    global _generated_hash_code_cache
    
    # Return cached code if available
    if commit_hash in _generated_hash_code_cache:
        return _generated_hash_code_cache[commit_hash]
    
    # Fun marketing words and phrases (ASCII only)
    marketing_words = [
        "CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE", "LAUNCH", "FLY",
        "SPARK", "SHINE", "GLOW", "RISE", "LEAP", "JUMP", "DASH", "ZOOM",
        "POWER", "MAGIC", "WONDER", "AMAZE", "THRILL", "EXCITE", "INSPIRE", "IGNITE",
        "ROCKET", "STAR", "MOON", "SUN", "OCEAN", "MOUNTAIN", "FOREST", "RIVER",
        "TECH", "AI", "CODE", "DATA", "SMART", "FAST", "SECURE", "TRUST",
        "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "GANG", "TRIBE", "CLAN"
    ]
    
    # Fun ASCII symbols and characters
    ascii_symbols = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
    
    # Generate a deterministic but fun password using the commit hash
    # Handle cases where commit_hash might contain non-hex characters
    try:
        if commit_hash != "unknown" and all(c in '0123456789abcdefABCDEF' for c in commit_hash):
            hash_num = int(commit_hash, 16)
        else:
            hash_num = hash(commit_hash)
    except ValueError:
        hash_num = hash(commit_hash)
    random.seed(hash_num)
    
    # Pick a random marketing word
    word = random.choice(marketing_words)
    
    # Pick a random ASCII symbol
    symbol = random.choice(ascii_symbols)
    
    # Generate a short number (2-3 digits)
    number = random.randint(10, 999)
    
    # Combine them in a fun way (ASCII only)
    password = f"{word}{number}{symbol}"
    
    # Cache the generated code
    _generated_hash_code_cache[commit_hash] = password
    
    return password

# Add a module-level flag to track if we've already printed the current code
_current_code_printed = False
_next_code_printed = False

def get_current_marketing_code():
    """
    Get the current live marketing code from database.
    This should only change after successful deployment.
    """
    global _current_code_printed
    
    try:
        # Try database first (cost-effective)
        database_connection_string = os.environ.get('DATABASE_CONNECTION_STRING')
        if database_connection_string:
            from scripts.database_client import DatabaseClient
            db_client = DatabaseClient(database_connection_string)
            current_code = db_client.get_current_marketing_code()
            
            if current_code:
                if not _current_code_printed:
                    print(f"✅ Using database current code: {current_code}")
                    _current_code_printed = True
                return current_code
            else:
                if not _current_code_printed:
                    print("⚠️ No current code found in database")
                    _current_code_printed = True
    except Exception as e:
        if not _current_code_printed:
            print(f"❌ Error accessing database: {e}")
            _current_code_printed = True
    
    # Fallback to Secret Manager (if database not available)
    try:
        from scripts.secret_manager_client import SecretManagerClient
        client = SecretManagerClient(os.environ.get('GOOGLE_CLOUD_PROJECT', 'yourl-cloud'))
        current_code = client.get_current_marketing_code()
        
        if current_code:
            if not _current_code_printed:
                print(f"✅ Using Secret Manager current code: {current_code}")
                _current_code_printed = True
            return current_code
        else:
            if not _current_code_printed:
                print("⚠️ No current code found in Secret Manager")
                _current_code_printed = True
            
    except Exception as e:
        if not _current_code_printed:
            print(f"❌ Error accessing Secret Manager: {e}")
            _current_code_printed = True
    
    # Fallback to environment variable
    build_password = os.environ.get('BUILD_MARKETING_CODE')
    if build_password:
        if not _current_code_printed:
            print(f"✅ Using BUILD_MARKETING_CODE: {build_password}")
            _current_code_printed = True
        return build_password
    
    # Last resort: generate based on current commit (should not happen in production)
    fallback_code = generate_marketing_code()
    if not _current_code_printed:
        print(f"⚠️ Using fallback generated code: {fallback_code}")
        _current_code_printed = True
    return fallback_code

def get_next_marketing_code():
    """
    Get the next marketing code from database.
    This is what will become the current code after next deployment.
    """
    global _next_code_printed
    
    try:
        # Try database first (cost-effective)
        database_connection_string = os.environ.get('DATABASE_CONNECTION_STRING')
        if database_connection_string:
            from scripts.database_client import DatabaseClient
            db_client = DatabaseClient(database_connection_string)
            next_code = db_client.get_next_marketing_code()
            
            if next_code:
                if not _next_code_printed:
                    print(f"✅ Using database next code: {next_code}")
                    _next_code_printed = True
                return next_code
            else:
                if not _next_code_printed:
                    print("⚠️ No next code found in database")
                    _next_code_printed = True
    except Exception as e:
        if not _next_code_printed:
            print(f"❌ Error accessing database: {e}")
            _next_code_printed = True
    
    # Fallback to Secret Manager (if database not available)
    try:
        from scripts.secret_manager_client import SecretManagerClient
        client = SecretManagerClient(os.environ.get('GOOGLE_CLOUD_PROJECT', 'yourl-cloud'))
        next_code = client.get_next_marketing_code()
        
        if next_code:
            if not _next_code_printed:
                print(f"✅ Using Secret Manager next code: {next_code}")
                _next_code_printed = True
            return next_code
        else:
            if not _next_code_printed:
                print("⚠️ No next code found in Secret Manager")
                _next_code_printed = True
            
    except Exception as e:
        if not _next_code_printed:
            print(f"❌ Error accessing Secret Manager: {e}")
            _next_code_printed = True
    
    # Fallback: generate next code based on current commit
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                            text=True, stderr=subprocess.DEVNULL).strip()[:8]
        next_hash = commit_hash + "_next"
    except:
        next_hash = "next_unknown"
    
    fallback_code = generate_marketing_code_from_hash(next_hash)
    if not _next_code_printed:
        print(f"⚠️ Using fallback generated next code: {fallback_code}")
        _next_code_printed = True
    return fallback_code

# Friends and Family Guard Ruleset
FRIENDS_FAMILY_GUARD = {
    "enabled": True,
    "visual_inspection": {
        "pc_allowed": True,
        "phone_allowed": True,
        "watch_blocked": True,
        "tablet_allowed": True
    },
    "session_id": "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
    "organization": "Yourl.Cloud Inc."
}

# Demo configuration for rapid prototyping (replace with proper auth/db for production)
DEMO_CONFIG = {
    "connections": [
        {
            "id": 1,
            "name": "GitHub Repository",
            "url": "https://github.com/XDM-ZSBW/yourl.cloud",
            "description": "Source code and documentation"
        },
        {
            "id": 2,
            "name": "Google Cloud Run",
            "url": "https://cloud.google.com/run",
            "description": "Deploy and scale applications"
        },
        {
            "id": 3,
            "name": "Flask Framework",
            "url": "https://flask.palletsprojects.com/",
            "description": "Python web framework"
        },
        {
            "id": 4,
            "name": "Perplexity AI",
            "url": "https://perplexity.ai",
            "description": "AI-powered search and assistance"
        },
        {
            "id": 5,
            "name": "Cursor IDE",
            "url": "https://cursor.sh",
            "description": "AI-powered code editor"
        }
    ]
}

# Configure Flask for Cloud Run domain mapping compatibility
app.config.update(
    # Trust X-Forwarded headers from Cloud Run proxy
    PREFERRED_URL_SCHEME='https',  # Cloud Run always serves HTTPS
    # Enable proxy support for X-Forwarded headers
    USE_X_SENDFILE=False,
    # Disable strict host checking for domain mapping compatibility
    SERVER_NAME=None
)

def get_client_ip():
    """
    Get the real client IP address, handling Cloud Run's X-Forwarded headers.
    Cloud Run sits behind a proxy, so we need to check X-Forwarded-For header.
    """
    # Check for X-Forwarded-For header (Cloud Run proxy)
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return x_forwarded_for.split(',')[0].strip()
    # Fallback to direct connection
    return request.remote_addr

def get_original_host():
    """
    Get the original host from X-Forwarded-Host header (Cloud Run domain mapping).
    Falls back to the request host if not available.
    """
    return request.headers.get('X-Forwarded-Host', request.host)

def get_original_protocol():
    """
    Get the original protocol from X-Forwarded-Proto header.
    Cloud Run always serves HTTPS, but we check the header for completeness.
    """
    return request.headers.get('X-Forwarded-Proto', 'https')

def detect_device_type(user_agent):
    """
    Detect device type based on User-Agent string.
    Returns: 'pc', 'phone', 'tablet', 'watch', 'unknown'
    """
    ua_lower = user_agent.lower()
    
    # Watch detection (blocked for visual inspection)
    if any(keyword in ua_lower for keyword in ['watch', 'wearable', 'smartwatch', 'apple watch', 'samsung gear']):
        return 'watch'
    
    # Phone detection
    if any(keyword in ua_lower for keyword in ['mobile', 'android', 'iphone', 'phone', 'blackberry']):
        return 'phone'
    
    # Tablet detection
    if any(keyword in ua_lower for keyword in ['tablet', 'ipad', 'android']):
        return 'tablet'
    
    # Default to PC
    return 'pc'

def is_visual_inspection_allowed(device_type):
    """
    Check if visual inspection is allowed for the given device type.
    """
    if not FRIENDS_FAMILY_GUARD["enabled"]:
        return True
    
    return FRIENDS_FAMILY_GUARD["visual_inspection"].get(f"{device_type}_allowed", False)

def get_visitor_data():
    """
    Get visitor tracking data for the current request.
    Returns visitor information for the landing page.
    """
    try:
        # Get visitor ID from session or generate one
        visitor_id = request.cookies.get('visitor_id')
        if not visitor_id:
            import uuid
            visitor_id = str(uuid.uuid4())
        
        # Check for session-based authentication (for when database is not available)
        session_authenticated = session.get('authenticated', False)
        session_access_code = session.get('last_access_code')
        
        # Try to get database connection
        database_connection = os.environ.get('DATABASE_CONNECTION_STRING')
        if database_connection:
            from scripts.database_client import DatabaseClient
            db_client = DatabaseClient(database_connection)
            
            # Get or create visitor record
            visitor = db_client.get_or_create_visitor(
                visitor_id=visitor_id,
                user_agent=request.headers.get('User-Agent'),
                ip_address=get_client_ip(),
                device_type=detect_device_type(request.headers.get('User-Agent', ''))
            )
            
            if visitor:
                return {
                    'visitor_id': visitor.get('visitor_id'),
                    'tracking_key': visitor.get('public_tracking_key'),
                    'last_access_code': visitor.get('last_access_code'),
                    'total_visits': visitor.get('total_visits', 1),
                    'is_new_visitor': visitor.get('total_visits', 1) == 1,
                    'has_used_code': visitor.get('last_access_code') is not None
                }
        
        # Fallback if database not available - use session data
        return {
            'visitor_id': visitor_id,
            'tracking_key': None,
            'last_access_code': session_access_code,
            'total_visits': 1,
            'is_new_visitor': not session_authenticated,
            'has_used_code': session_authenticated
        }
        
    except Exception as e:
        print(f"⚠️ Error getting visitor data: {e}")
        return {
            'visitor_id': request.cookies.get('visitor_id', 'unknown'),
            'tracking_key': None,
            'last_access_code': session.get('last_access_code'),
            'total_visits': 1,
            'is_new_visitor': not session.get('authenticated', False),
            'has_used_code': session.get('authenticated', False)
        }

@app.route('/', methods=['GET', 'POST'])
def main_endpoint():
    """
    Main endpoint that handles both GET (landing page) and POST (authentication).
    Compatible with Cloud Run domain mappings with visitor tracking.
    """
    if request.method == 'GET':
        # Get current marketing code
        current_password = get_current_marketing_code()
        
        # Get visitor information
        visitor_data = get_visitor_data()
        
        # Check for authentication error in session
        auth_error = session.get('auth_error')
        show_tutorial = request.args.get('error') == 'auth_failed'
        
        # Clear the error from session after displaying
        if auth_error:
            session.pop('auth_error', None)
        
        # Create response with no-cache headers to ensure fresh content
        if os.path.exists('templates/index.html'):
            response = make_response(render_template('index.html', 
                                                 marketing_code=current_password,
                                                 visitor_data=visitor_data,
                                                 auth_error=auth_error,
                                                 show_tutorial=show_tutorial))
        else:
            # Build error message and tutorial HTML
            error_html = ""
            tutorial_html = ""
            
            if auth_error:
                error_html = f"""
                <div class="error-message" style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center;">
                    <strong>❌ {auth_error['message']}</strong><br>
                    <small>Current code: <code style="background: #fff3cd; padding: 2px 6px; border-radius: 3px;">{auth_error['current_code']}</code></small>
                </div>
                """
            
            if show_tutorial:
                tutorial_html = f"""
                <div class="tutorial-container" style="background: #d1ecf1; border: 1px solid #bee5eb; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #0c5460; text-align: center; margin-top: 0;">🎯 How to Get Your Marketing Code</h3>
                    
                    <div class="tutorial-steps" style="display: flex; flex-direction: column; gap: 15px;">
                        <div class="step" style="display: flex; align-items: center; gap: 10px; padding: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div class="step-number" style="background: #007bff; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">1</div>
                            <div class="step-content">
                                <strong>Copy the Current Code:</strong> 
                                <div class="code-display" style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 8px; border-radius: 5px; margin: 5px 0; font-family: monospace; font-size: 16px; text-align: center; cursor: pointer;" onclick="copyToClipboard('{current_password}')" title="Click to copy">
                                    {current_password}
                                </div>
                            </div>
                        </div>
                        
                        <div class="step" style="display: flex; align-items: center; gap: 10px; padding: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div class="step-number" style="background: #28a745; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">2</div>
                            <div class="step-content">
                                <strong>Paste into the Code Box:</strong> 
                                <div class="paste-animation" style="text-align: center; margin: 5px 0;">
                                    <span class="arrow" style="font-size: 20px; animation: arrow 2s infinite;">➡️</span>
                                    <span class="input-box" style="font-size: 20px; animation: input 2s infinite;">📝</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="step" style="display: flex; align-items: center; gap: 10px; padding: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <div class="step-number" style="background: #ffc107; color: #212529; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">3</div>
                            <div class="step-content">
                                <strong>Click the Launch Button:</strong> 
                                <div class="button-animation" style="text-align: center; margin: 5px 0;">
                                    <span class="button-icon" style="font-size: 20px; animation: button 2s infinite;">🚀</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="tutorial-note" style="text-align: center; margin-top: 15px; font-style: italic; color: #6c757d;">
                        💡 <strong>Pro Tip:</strong> The marketing code changes with each deployment, so always use the current one shown above!
                    </div>
                </div>
                
                <style>
                    @keyframes paste {{
                        0%, 100% {{ transform: scale(1); opacity: 1; }}
                        50% {{ transform: scale(1.2); opacity: 0.8; }}
                    }}
                    @keyframes arrow {{
                        0%, 100% {{ transform: translateX(0); opacity: 1; }}
                        50% {{ transform: translateX(10px); opacity: 0.6; }}
                    }}
                    @keyframes input {{
                        0%, 100% {{ transform: scale(1); opacity: 1; }}
                        50% {{ transform: scale(1.1); opacity: 0.8; }}
                    }}
                    @keyframes button {{
                        0%, 100% {{ transform: scale(1); opacity: 1; }}
                        50% {{ transform: scale(1.3); opacity: 0.8; }}
                    }}
                    .code-display:hover {{
                        background: #ffeaa7 !important;
                        transform: scale(1.02);
                        transition: all 0.2s ease;
                    }}
                </style>
                
                <script>
                    function copyToClipboard(text) {{
                        navigator.clipboard.writeText(text).then(function() {{
                            // Show success feedback
                            const codeDisplay = document.querySelector('.code-display');
                            const originalText = codeDisplay.textContent;
                            codeDisplay.textContent = '✅ Copied!';
                            codeDisplay.style.background = '#d4edda';
                            codeDisplay.style.color = '#155724';
                            
                            setTimeout(() => {{
                                codeDisplay.textContent = originalText;
                                codeDisplay.style.background = '#fff3cd';
                                codeDisplay.style.color = '#856404';
                            }}, 1500);
                        }}).catch(function(err) {{
                            console.error('Could not copy text: ', err);
                        }});
                    }}
                </script>
                """
            
            response = make_response(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Yourl.Cloud - URL API Server</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; text-align: center; }}
                .form-group {{ margin: 20px 0; }}
                label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }}
                button {{ background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                button:hover {{ background: #0056b3; }}
                .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .password-display {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin: 10px 0; text-align: center; font-weight: bold; }}
                .error-message {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Yourl.Cloud</h1>
                <div class="info">
                    <strong>URL API Server with Visual Inspection</strong><br>
                    Production-ready Flask application with security features.<br>
                    <strong>Domain:</strong> {get_original_host()}<br>
                    <strong>Protocol:</strong> {get_original_protocol()}
                </div>
                
                {error_html}
                {tutorial_html}
                
                <form method="POST">
                    <div class="form-group">
                        <label for="password">🎯 Marketing Password:</label>
                        <input type="text" id="password" name="password" placeholder="Enter the fun marketing password" value="" required>
                    </div>
                    <button type="submit">🚀 Launch Experience</button>
                </form>
                <div class="password-display">
                    <strong>🎪 Current Marketing Password:</strong> {current_password}
                </div>
                <div class="info">
                    <strong>Health Check:</strong> <a href="/health">/health</a><br>
                    <strong>Status:</strong> <a href="/status">/status</a>
                </div>
            </div>
        </body>
        </html>
        """)
        
        # Add cache control headers to prevent browser caching
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    elif request.method == 'POST':
        # Handle authentication with simple password check
        password = request.form.get('password', '')
        current_password = get_current_marketing_code()
        
        if password == current_password:
            # Set session-based authentication (for when database is not available)
            session['authenticated'] = True
            session['last_access_code'] = current_password
            
            # Get the next code for authenticated users (Cursor ownership)
            next_password = get_next_marketing_code()
            
            # Log successful authentication to database if available
            try:
                database_connection = os.environ.get('DATABASE_CONNECTION_STRING')
                if database_connection:
                    from scripts.database_client import DatabaseClient
                    db_client = DatabaseClient(database_connection)
                    
                    # Log usage
                    db_client.log_usage(current_password, request.headers.get('User-Agent'), 
                                      get_client_ip(), '/auth', True)
                    
                    # Log visitor access
                    visitor_id = request.cookies.get('visitor_id')
                    if visitor_id:
                        db_client.log_visitor_access(
                            visitor_id=visitor_id,
                            access_code=current_password,
                            success=True,
                            user_agent=request.headers.get('User-Agent'),
                            ip_address=get_client_ip()
                        )
            except Exception as e:
                print(f"⚠️ Database logging failed: {e}")
            
            # Get current build version/commit hash
            try:
                build_version = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                                     text=True, stderr=subprocess.DEVNULL).strip()[:8]
            except:
                build_version = "unknown"
            
            # Get visitor data for personalization
            visitor_data = get_visitor_data()
            visitor_id = visitor_data.get('visitor_id', 'unknown')
            
            # Store landing page version in SQL if database is available
            landing_page_version = None
            try:
                database_connection = os.environ.get('DATABASE_CONNECTION_STRING')
                if database_connection:
                    from scripts.database_client import DatabaseClient
                    db_client = DatabaseClient(database_connection)
                    
                    # Store landing page version
                    landing_page_url = f"{get_original_protocol()}://{get_original_host()}/"
                    db_client.store_landing_page_version(
                        visitor_id=visitor_id,
                        landing_page_url=landing_page_url,
                        build_version=build_version,
                        marketing_code=current_password
                    )
                    
                    # Get visitor's landing page history for personalization
                    landing_page_version = db_client.get_landing_page_version(visitor_id)
            except Exception as e:
                print(f"⚠️ Database logging failed: {e}")
                landing_page_version = None
            
            # Create personalized response based on visitor data
            is_new_visitor = visitor_data.get('is_new_visitor', True)
            has_used_code = visitor_data.get('has_used_code', False)
            total_visits = visitor_data.get('total_visits', 1)
            
            # Personalize the experience
            if is_new_visitor:
                welcome_message = "🎉 Welcome to Yourl.Cloud! This is your first visit!"
                experience_level = "new_user"
            elif has_used_code:
                welcome_message = f"🎯 Welcome back! This is visit #{total_visits} and you've successfully used a code before!"
                experience_level = "returning_user"
            else:
                welcome_message = f"👋 Welcome back! This is visit #{total_visits}!"
                experience_level = "returning_visitor"
            
            # Create JSON response with actual URL and personalized data
            json_response = {
                "status": "authenticated",
                "message": welcome_message,
                "experience_level": experience_level,
                "visitor_data": {
                    "visitor_id": visitor_id,
                    "total_visits": total_visits,
                    "is_new_visitor": is_new_visitor,
                    "has_used_code": has_used_code,
                    "tracking_key": visitor_data.get('tracking_key')
                },
                "landing_page": {
                    "url": f"{get_original_protocol()}://{get_original_host()}/",
                    "build_version": build_version,
                    "marketing_code": current_password
                },
                "current_marketing_code": current_password,
                "next_marketing_code": next_password,
                "ownership": {
                    "perplexity": "current_marketing_code",
                    "cursor": "next_marketing_code"
                },
                "navigation": {
                    "back_to_landing": f"{get_original_protocol()}://{get_original_host()}/",
                    "api_endpoint": f"{get_original_protocol()}://{get_original_host()}/api",
                    "status_page": f"{get_original_protocol()}://{get_original_host()}/status"
                },
                "timestamp": datetime.utcnow().isoformat(),
                "organization": FRIENDS_FAMILY_GUARD["organization"]
            }
            
            # Add landing page version history if available
            if landing_page_version:
                json_response["landing_page"]["version_history"] = {
                    "first_accessed": landing_page_version.get('first_accessed_at'),
                    "last_accessed": landing_page_version.get('last_accessed_at'),
                    "access_count": landing_page_version.get('access_count'),
                    "previous_url": landing_page_version.get('landing_page_url')
                }
            
            # Instead of returning HTML directly, redirect to prevent form resubmission
            # Store authentication data in session for the redirected page
            session['auth_data'] = {
                'welcome_message': welcome_message,
                'experience_level': experience_level,
                'visitor_data': {
                    'visitor_id': visitor_id,
                    'total_visits': total_visits,
                    'is_new_visitor': is_new_visitor,
                    'has_used_code': has_used_code,
                    'tracking_key': visitor_data.get('tracking_key')
                },
                'landing_page': {
                    'url': f"{get_original_protocol()}://{get_original_host()}/",
                    'build_version': build_version,
                    'marketing_code': current_password
                },
                'current_marketing_code': current_password,
                'next_marketing_code': next_password,
                'ownership': {
                    'perplexity': 'current_marketing_code',
                    'cursor': 'next_marketing_code'
                },
                'navigation': {
                    'back_to_landing': f"{get_original_protocol()}://{get_original_host()}/",
                    'api_endpoint': f"{get_original_protocol()}://{get_original_host()}/api",
                    'status_page': f"{get_original_protocol()}://{get_original_host()}/status"
                },
                'timestamp': datetime.utcnow().isoformat(),
                'organization': FRIENDS_FAMILY_GUARD["organization"]
            }
            
            # Add landing page version history if available
            if landing_page_version:
                session['auth_data']["landing_page"]["version_history"] = {
                    'first_accessed': landing_page_version.get('first_accessed_at'),
                    'last_accessed': landing_page_version.get('last_accessed_at'),
                    'access_count': landing_page_version.get('access_count'),
                    'previous_url': landing_page_version.get('landing_page_url')
                }
            
            # Redirect to prevent form resubmission (PRG pattern)
            return redirect('/authenticated', code=302)
        else:
            # Handle failed authentication - redirect to home with error message
            session['auth_error'] = {
                'message': 'Invalid password. Please try again.',
                'current_code': current_password,
                'timestamp': datetime.utcnow().isoformat()
            }
            return redirect('/?error=auth_failed', code=302)
    
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def get_request_url():
    """
    API endpoint that returns the request URL and metadata.
    Compatible with Cloud Run domain mappings.
    """
    # Get request information with Cloud Run header support
    url = request.url
    method = request.method
    headers = dict(request.headers)
    user_agent = headers.get('User-Agent', 'Unknown')
    device_type = detect_device_type(user_agent)
    
    # Get Cloud Run specific information
    client_ip = get_client_ip()
    original_host = get_original_host()
    original_protocol = get_original_protocol()
    
    # Check if visual inspection is allowed
    if is_visual_inspection_allowed(device_type):
        # Return HTML for allowed devices
        return render_visual_inspection(url, device_type, datetime.utcnow(), original_host, original_protocol)
    else:
        # Return JSON for blocked devices (like watches)
        return jsonify({
            "url": url,
            "method": method,
            "device_type": device_type,
            "visual_inspection": "blocked",
            "timestamp": datetime.utcnow().isoformat(),
            "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
            "organization": FRIENDS_FAMILY_GUARD["organization"],
            "cloud_run": {
                "client_ip": client_ip,
                "original_host": original_host,
                "original_protocol": original_protocol,
                "domain_mapping_enabled": CLOUD_RUN_CONFIG["domain_mapping_enabled"]
            }
        })

def render_visual_inspection(url, device_type, timestamp, original_host, original_protocol):
    """
    Render the visual inspection interface for allowed devices.
    Enhanced for Cloud Run domain mapping compatibility.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yourl.Cloud - Visual Inspection</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
                font-weight: 300;
            }}
            .content {{
                padding: 30px;
            }}
            .url-display {{
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                word-break: break-all;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .info-card {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                border-left: 4px solid #007bff;
            }}
            .info-card h3 {{
                margin: 0 0 10px 0;
                color: #007bff;
            }}
            .status-badge {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }}
            .status-success {{
                background: #d4edda;
                color: #155724;
            }}
            .status-info {{
                background: #d1ecf1;
                color: #0c5460;
            }}
            .refresh-btn {{
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                transition: transform 0.2s;
            }}
            .refresh-btn:hover {{
                transform: translateY(-2px);
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-top: 1px solid #e9ecef;
            }}
            @media (max-width: 768px) {{
                .container {{
                    margin: 10px;
                    border-radius: 10px;
                }}
                .header h1 {{
                    font-size: 2em;
                }}
                .content {{
                    padding: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Visual Inspection</h1>
                <p>Yourl.Cloud URL API Server - Real-time Monitoring</p>
            </div>
            
            <div class="content">
                <div class="url-display">
                    <strong>Request URL:</strong><br>
                    {url}
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>📱 Device Information</h3>
                        <p><strong>Type:</strong> {device_type.title()}</p>
                        <p><strong>Status:</strong> <span class="status-badge status-success">Allowed</span></p>
                    </div>
                    
                    <div class="info-card">
                        <h3>🛡️ Security Status</h3>
                        <p><strong>Guard:</strong> <span class="status-badge status-success">Enabled</span></p>
                        <p><strong>Inspection:</strong> <span class="status-badge status-info">Active</span></p>
                    </div>
                    
                    <div class="info-card">
                        <h3>⏰ Timestamp</h3>
                        <p><strong>Time:</strong> {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                        <p><strong>Session:</strong> {FRIENDS_FAMILY_GUARD['session_id'][:8]}...</p>
                    </div>
                    
                    <div class="info-card">
                        <h3>🏢 Organization</h3>
                        <p><strong>Company:</strong> {FRIENDS_FAMILY_GUARD['organization']}</p>
                        <p><strong>Environment:</strong> <span class="status-badge status-success">Production</span></p>
                    </div>
                    
                    <div class="info-card">
                        <h3>☁️ Cloud Run Info</h3>
                        <p><strong>Domain:</strong> {original_host}</p>
                        <p><strong>Protocol:</strong> {original_protocol}</p>
                        <p><strong>Mapping:</strong> <span class="status-badge status-success">Enabled</span></p>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <button class="refresh-btn" onclick="location.reload()">
                        🔄 Refresh Data
                    </button>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Yourl.Cloud</strong> - Secure URL API Server with Visual Inspection</p>
                <p>Session: {FRIENDS_FAMILY_GUARD['session_id']} | Organization: {FRIENDS_FAMILY_GUARD['organization']}</p>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 30 seconds
            setTimeout(function() {{
                location.reload();
            }}, 30000);
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Cloud Run domain mapping compatibility.
    This endpoint is used by Cloud Run for health checks and domain mapping validation.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "url-api",
        "version": "1.0.0",
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "cloud_run_support": True,
        "domain_mapping": {
            "enabled": CLOUD_RUN_CONFIG["domain_mapping_enabled"],
            "region": CLOUD_RUN_CONFIG["region"],
            "health_check_path": CLOUD_RUN_CONFIG["health_check_path"]
        },
        "wsgi_server": "waitress" if platform.system() == "Windows" else "gunicorn",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "port": PORT,
        "host": get_original_host(),
        "protocol": get_original_protocol()
    })

@app.route('/status', methods=['GET'])
def status():
    """
    Status endpoint with service information.
    Enhanced for Cloud Run domain mapping compatibility.
    """
    return jsonify({
        "service": "URL API with Visual Inspection",
        "version": "1.0.0",
        "status": "running",
        "port": PORT,
        "host": get_original_host(),
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": FRIENDS_FAMILY_GUARD["session_id"],
        "organization": FRIENDS_FAMILY_GUARD["organization"],
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "visual_inspection": FRIENDS_FAMILY_GUARD["visual_inspection"],
        "cloud_run_support": True,
        "demo_mode": True,
        "wsgi_server": "waitress" if platform.system() == "Windows" else "gunicorn",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "domain_mapping": {
            "enabled": CLOUD_RUN_CONFIG["domain_mapping_enabled"],
            "region": CLOUD_RUN_CONFIG["region"],
            "original_host": get_original_host(),
            "original_protocol": get_original_protocol(),
            "client_ip": get_client_ip()
        }
    })

@app.route('/guard', methods=['GET'])
def guard_status():
    """
    Friends and Family Guard status endpoint.
    """
    return jsonify({
        "friends_family_guard": FRIENDS_FAMILY_GUARD,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/data', methods=['GET'])
def data_stream():
    """
    Enhanced data stream endpoint providing vertical linear datastream with horizontally scrollable wiki stories.
    Each frame represents a story interpretation of the vertical scroll area with mind map navigation.
    Only accessible to authenticated users who have previously used a valid code.
    """
    # Get visitor data for personalization
    visitor_data = get_visitor_data()
    
    # Check if visitor has authenticated (used a valid code previously)
    if not visitor_data.get('has_used_code', False):
        return make_response(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Denied - Data Stream</title>
            <style>
                body {{ 
                    font-family: 'Courier New', monospace;
                    background: #000;
                    color: #ff0000;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                }}
                .access-denied {{
                    text-align: center;
                    padding: 40px;
                    border: 2px solid #ff0000;
                    border-radius: 10px;
                    background: rgba(255, 0, 0, 0.1);
                }}
                .error-code {{
                    font-size: 3rem;
                    margin-bottom: 20px;
                    text-shadow: 0 0 20px #ff0000;
                }}
                .message {{
                    font-size: 1.2rem;
                    margin-bottom: 30px;
                }}
                .nav-btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    background: #ff0000;
                    color: #000;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 10px;
                }}
                .nav-btn:hover {{
                    background: #cc0000;
                    color: #fff;
                }}
            </style>
        </head>
        <body>
            <div class="access-denied">
                <div class="error-code">🔒 ACCESS DENIED</div>
                <div class="message">
                    <p><strong>Data Stream Access Restricted</strong></p>
                    <p>This endpoint is only accessible to authenticated users.</p>
                    <p>You must first use a valid marketing code on the landing page.</p>
                    <p>Visitor ID: {visitor_data.get('visitor_id', 'Unknown')}</p>
                    <p>Authentication Status: Not Authenticated</p>
                </div>
                <div>
                    <a href="/" class="nav-btn">🏠 Return to Landing Page</a>
                    <a href="/status" class="nav-btn">📊 Service Status</a>
                </div>
            </div>
        </body>
        </html>
        """, 403)
    
    # Generate dynamic story frames based on current time and visitor data
    import time
    current_time = time.time()
    
    # Create comprehensive story frames with wiki interpretations
    story_frames = [
        {
            "id": "frame_001",
            "timestamp": current_time - 3600,  # 1 hour ago
            "title": "The Trust-Based AI Revolution",
            "content": "Yourl.Cloud Inc. stands at the forefront of a new era - the Trust-Based AI Revolution. We're not just building technology; we're creating a foundation of trust that enables AI to serve families across locations with integrity and reliability.",
            "category": "vision_future",
            "visual_elements": ["ai_trust", "family_bridge", "location_spanning"],
            "scroll_position": 0,
            "wiki_links": ["ARCHITECTURE_OVERVIEW.md", "BUSINESS_NAME_UPDATE.md"],
            "mind_map_nodes": ["trust", "ai", "family", "innovation"]
        },
        {
            "id": "frame_002", 
            "timestamp": current_time - 1800,  # 30 minutes ago
            "title": "The Clipboard Bridge Phenomenon",
            "content": "At cb.yourl.cloud, we've created something extraordinary - a clipboard bridge that transcends physical boundaries. AI assistants can now share context seamlessly across family locations, creating a unified experience that feels like magic.",
            "category": "breakthrough_technology",
            "visual_elements": ["clipboard_bridge", "context_sharing", "seamless_experience"],
            "scroll_position": 100,
            "wiki_links": ["CLIPBOARD_BRIDGE_DEPLOYMENT.md", "ZAIDO_CLIPBOARD_RECOVERY_GUIDE.md"],
            "mind_map_nodes": ["clipboard", "bridge", "context", "unified"]
        },
        {
            "id": "frame_003",
            "timestamp": current_time - 900,  # 15 minutes ago
            "title": "The Zaido Integration",
            "content": f"Visitor {visitor_data.get('visitor_id', 'Unknown')} is experiencing the power of Zaido integration. The Windows Focus Enhancer and clipboard tools work in harmony with Yourl.Cloud, creating a productivity ecosystem that adapts to individual needs.",
            "category": "ecosystem_integration",
            "visual_elements": ["zaido_tools", "focus_enhancer", "productivity_ecosystem"],
            "scroll_position": 200,
            "wiki_links": ["WINDOWS_CLIPBOARD_HISTORY_INTEGRATION.md", "ZAIDO_CLIPBOARD_CONFLICT_RESOLVER.md"],
            "mind_map_nodes": ["zaido", "integration", "productivity", "focus"]
        },
        {
            "id": "frame_004",
            "timestamp": current_time - 300,  # 5 minutes ago
            "title": "The Emergency Response System",
            "content": "In times of crisis, every second counts. Yourl.Cloud's emergency protocol activates instantly, connecting family members across locations, queuing AI assistants, and ensuring no one faces challenges alone.",
            "category": "emergency_support",
            "visual_elements": ["emergency_protocol", "family_connection", "ai_queue"],
            "scroll_position": 300,
            "wiki_links": ["SECURITY.md", "EMERGENCY_PROTOCOL.md"],
            "mind_map_nodes": ["emergency", "response", "family", "support"]
        },
        {
            "id": "frame_005",
            "timestamp": current_time,
            "title": "The Real-Time Knowledge Hub",
            "content": "Knowledge flows like a living river through our system. Every interaction, every decision, every moment contributes to a growing repository of wisdom that guides families toward better outcomes.",
            "category": "knowledge_evolution",
            "visual_elements": ["knowledge_river", "living_wisdom", "family_guidance"],
            "scroll_position": 400,
            "wiki_links": ["KNOWLEDGE_HUB.md", "WIKI_UPDATE_SYSTEM.md"],
            "mind_map_nodes": ["knowledge", "wisdom", "guidance", "evolution"]
        }
    ]
    
    # Add personalized frames based on visitor data
    if visitor_data.get('has_used_code', False):
        story_frames.append({
            "id": "frame_personal",
            "timestamp": current_time + 60,
            "title": "The Authenticated Path",
            "content": f"This visitor has walked the path of authentication. Their journey through the digital landscape has granted them access to deeper layers of the story, revealing secrets hidden in plain sight.",
            "category": "personal_privilege",
            "visual_elements": ["authenticated_path", "hidden_secrets", "deeper_layers"],
            "scroll_position": 500,
            "wiki_links": ["SECURITY.md", "SECURITY_CHECKLIST.md"],
            "mind_map_nodes": ["authentication", "security", "access"]
        })
    
    if visitor_data.get('total_visits', 1) > 1:
        story_frames.append({
            "id": "frame_returning",
            "timestamp": current_time + 120,
            "title": "The Returning Wanderer",
            "content": f"Like a traveler returning to familiar lands, this visitor has walked these digital paths before. Their {visitor_data.get('total_visits', 1)} visits have woven them into the fabric of this digital story.",
            "category": "returning_visitor",
            "visual_elements": ["familiar_lands", "woven_fabric", "digital_story"],
            "scroll_position": 600,
            "wiki_links": ["WIKI_UPDATE_SUMMARY.md", "BETA_LAUNCH_SUMMARY.md"],
            "mind_map_nodes": ["returning", "familiarity", "history"]
        })
    
    # Add knowledge hub frame
    story_frames.append({
        "id": "frame_knowledge",
        "timestamp": current_time + 180,
        "title": "The Knowledge Hub",
        "content": "At the heart of this digital ecosystem lies the Knowledge Hub - a comprehensive repository of wisdom, experience, and insights that guides every decision and shapes every interaction.",
        "category": "knowledge_management",
        "visual_elements": ["knowledge_hub", "wisdom_repository", "insight_ecosystem"],
        "scroll_position": 700,
        "wiki_links": ["KNOWLEDGE_HUB.md", "WIKI_UPDATE_SYSTEM.md"],
        "mind_map_nodes": ["knowledge", "wisdom", "insights"]
    })
    
    # Add local development and build testing frame
    story_frames.append({
        "id": "frame_build_testing",
        "timestamp": current_time + 240,
        "title": "The Build Testing Phase",
        "content": "Right now, we're in the critical build testing phase. This local instance at localhost:60731 is our proving ground - where we validate every feature, test every integration, and ensure the Yourl.Cloud experience is flawless before deployment.",
        "category": "development_phase",
        "visual_elements": ["build_testing", "local_validation", "quality_assurance"],
        "scroll_position": 800,
        "wiki_links": ["LOCAL_DEVELOPMENT_SETUP.md", "BUILD_COMPLETE.md"],
        "mind_map_nodes": ["build", "testing", "validation", "quality"]
    })
    
    # Create the enhanced HTML response with vertical datastream and mind map
    # Generate mind map nodes HTML
    mind_map_nodes_html = ""
    for frame in story_frames:
        for node in frame.get('mind_map_nodes', []):
            mind_map_nodes_html += f'<div class="mind-map-node" onclick="filterByNode(\'{node}\')">{node.replace("_", " ").title()}</div>'
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Stream - Yourl.Cloud Inc.</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Courier New', monospace;
                background: #000;
                color: #00ff00;
                overflow-x: auto;
                overflow-y: hidden;
            }}
            .datastream-container {{
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                width: max-content;
                padding: 20px;
            }}
            .frame {{
                width: 800px;
                min-height: 300px;
                margin: 20px 0;
                padding: 30px;
                background: rgba(0, 255, 0, 0.05);
                border: 1px solid #00ff00;
                border-radius: 10px;
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
            }}
            .frame::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, #00ff00, #00aa00, #00ff00);
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0% {{ opacity: 0.5; }}
                50% {{ opacity: 1; }}
                100% {{ opacity: 0.5; }}
            }}
            .frame:hover {{
                background: rgba(0, 255, 0, 0.1);
                transform: scale(1.02);
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            }}
            .frame-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(0, 255, 0, 0.3);
            }}
            .frame-id {{
                font-weight: bold;
                color: #00aa00;
            }}
            .frame-timestamp {{
                font-size: 0.9rem;
                color: #00aa00;
            }}
            .frame-category {{
                display: inline-block;
                padding: 5px 10px;
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                border-radius: 5px;
                font-size: 0.8rem;
                margin-bottom: 10px;
            }}
            .frame-title {{
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 15px;
                color: #00ff00;
            }}
            .frame-content {{
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            .visual-elements {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-bottom: 15px;
            }}
            .visual-element {{
                padding: 5px 10px;
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                border-radius: 5px;
                font-size: 0.8rem;
            }}
            .wiki-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(0, 255, 0, 0.3);
            }}
            .wiki-link {{
                padding: 5px 10px;
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                border-radius: 5px;
                font-size: 0.8rem;
                text-decoration: none;
                color: #00ff00;
                transition: all 0.3s ease;
            }}
            .wiki-link:hover {{
                background: rgba(0, 255, 0, 0.3);
                transform: scale(1.05);
            }}
            .mind-map {{
                position: fixed;
                top: 20px;
                right: 20px;
                width: 300px;
                height: 400px;
                background: rgba(0, 0, 0, 0.9);
                border: 1px solid #00ff00;
                border-radius: 10px;
                padding: 15px;
                z-index: 1000;
            }}
            .mind-map-title {{
                text-align: center;
                font-size: 1.2rem;
                margin-bottom: 15px;
                color: #00ff00;
            }}
            .mind-map-node {{
                display: inline-block;
                padding: 5px 10px;
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                border-radius: 5px;
                font-size: 0.8rem;
                margin: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .mind-map-node:hover {{
                background: rgba(0, 255, 0, 0.4);
                transform: scale(1.1);
            }}
            .scroll-indicator {{
                position: fixed;
                top: 20px;
                left: 20px;
                background: rgba(0, 0, 0, 0.8);
                padding: 10px;
                border: 1px solid #00ff00;
                border-radius: 5px;
                font-size: 0.9rem;
            }}
            .navigation {{
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
            }}
            .nav-btn {{
                padding: 10px 20px;
                background: #00ff00;
                color: #000;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            .nav-btn:hover {{
                background: #00aa00;
                color: #fff;
                transform: scale(1.05);
            }}
            .visitor-info {{
                position: fixed;
                top: 20px;
                left: 20px;
                background: rgba(0, 0, 0, 0.8);
                padding: 15px;
                border: 1px solid #00ff00;
                border-radius: 5px;
                font-size: 0.9rem;
            }}
            .data-stream-title {{
                text-align: center;
                font-size: 2rem;
                margin-bottom: 30px;
                color: #00ff00;
                text-shadow: 0 0 20px #00ff00;
            }}
            .mind-map-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }}
            .build-checklist {{
                position: fixed;
                bottom: 100px;
                right: 20px;
                width: 350px;
                background: rgba(0, 0, 0, 0.9);
                border: 1px solid #00ff00;
                border-radius: 10px;
                padding: 15px;
                z-index: 1000;
            }}
            .build-checklist h4 {{
                text-align: center;
                margin-bottom: 15px;
                color: #00ff00;
            }}
            .checklist-item {{
                display: flex;
                align-items: center;
                margin: 8px 0;
                padding: 5px;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .checklist-item:hover {{
                background: rgba(0, 255, 0, 0.1);
            }}
            .checklist-item input[type="checkbox"] {{
                margin-right: 10px;
                accent-color: #00ff00;
            }}
            .checklist-item.completed {{
                color: #00aa00;
                text-decoration: line-through;
            }}
        </style>
    </head>
    <body>
        <div class="visitor-info">
            <h3>👤 Visitor Data</h3>
            <p><strong>ID:</strong> {visitor_data.get('visitor_id', 'Unknown')}</p>
            <p><strong>Visits:</strong> {visitor_data.get('total_visits', 1)}</p>
            <p><strong>Status:</strong> {'Returning' if not visitor_data.get('is_new_visitor', True) else 'New'}</p>
            <p><strong>Code Usage:</strong> {'Yes' if visitor_data.get('has_used_code', False) else 'No'}</p>
            <hr style="border-color: #00ff00; margin: 10px 0;">
            <h4>🏗️ Build Status</h4>
            <p><strong>Environment:</strong> Local Development</p>
            <p><strong>Instance:</strong> localhost:60731</p>
            <p><strong>Mode:</strong> Build Testing</p>
            <p><strong>Status:</strong> 🟢 Active</p>
        </div>
        
        <div class="mind-map">
            <div class="mind-map-title">🧠 Mind Map</div>
            <div class="mind-map-container">
                {mind_map_nodes_html}
            </div>
        </div>
        
        <div class="build-checklist">
            <h4>✅ Build Testing Checklist</h4>
            <div class="checklist-item">
                <input type="checkbox" id="check1" onchange="updateChecklist(this)">
                <label for="check1">Local server running</label>
            </div>
            <div class="checklist-item">
                <input type="checkbox" id="check2" onchange="updateChecklist(this)">
                <label for="check2">Data endpoint accessible</label>
            </div>
            <div class="checklist-item">
                <input type="checkbox" id="check3" onchange="updateChecklist(this)">
                <label for="check3">Story frames displaying</label>
            </div>
            <div class="checklist-item">
                <input type="checkbox" id="check4" onchange="updateChecklist(this)">
                <label for="check4">Mind map interactive</label>
            </div>
            <div class="checklist-item">
                <input type="checkbox" id="check5" onchange="updateChecklist(this)">
                <label for="check5">Navigation working</label>
            </div>
            <div class="checklist-item">
                <input type="checkbox" id="check6" onchange="updateChecklist(this)">
                <label for="check6">Responsive design</label>
            </div>
        </div>
        
        <div class="scroll-indicator">
            <p><strong>Scroll Position:</strong> <span id="scrollPos">0</span></p>
            <p><strong>Frames:</strong> {len(story_frames)}</p>
            <p><strong>Categories:</strong> {len(set(frame['category'] for frame in story_frames))}</p>
        </div>
        
        <div class="datastream-container">
            <div class="data-stream-title">🚀 YOURL.CLOUD TRUST-BASED AI DATASTREAM</div>
            
            {''.join([f'''
            <div class="frame" data-scroll="{frame['scroll_position']}" data-category="{frame['category']}" data-nodes="{','.join(frame.get('mind_map_nodes', []))}">
                <div class="frame-header">
                    <span class="frame-id">{frame['id']}</span>
                    <span class="frame-timestamp">{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(frame['timestamp']))}</span>
                </div>
                <div class="frame-category">{frame['category'].replace('_', ' ').title()}</div>
                <div class="frame-title">{frame['title']}</div>
                <div class="frame-content">{frame['content']}</div>
                <div class="visual-elements">
                    {''.join([f'<span class="visual-element">{element.replace("_", " ").title()}</span>' for element in frame['visual_elements']])}
                </div>
                <div class="wiki-links">
                    {''.join([f'<a href="/wiki/{link}" class="wiki-link" target="_blank">📚 {link.replace(".md", "").replace("_", " ").title()}</a>' for link in frame.get('wiki_links', [])])}
                </div>
            </div>
            ''' for frame in story_frames])}
        </div>
        
        <div class="navigation">
            <a href="/" class="nav-btn">🏠 Home</a>
            <a href="/api" class="nav-btn">🔌 API</a>
            <a href="/status" class="nav-btn">📊 Status</a>
            <a href="/data" class="nav-btn">📡 Data Stream</a>
            <a href="/wiki/KNOWLEDGE_HUB.md" class="nav-btn" target="_blank">🧠 Knowledge Hub</a>
        </div>
        
        <script>
            // Update scroll position indicator
            window.addEventListener('scroll', function() {{
                document.getElementById('scrollPos').textContent = Math.round(window.scrollY);
            }});
            
            // Add hover effects to frames
            document.querySelectorAll('.frame').forEach(frame => {{
                frame.addEventListener('mouseenter', function() {{
                    this.style.background = 'rgba(0, 255, 0, 0.1)';
                    this.style.transform = 'scale(1.02)';
                }});
                
                frame.addEventListener('mouseleave', function() {{
                    this.style.background = 'rgba(0, 255, 0, 0.05)';
                    this.style.transform = 'scale(1)';
                }});
            }});
            
            // Mind map filtering
            function filterByNode(node) {{
                const frames = document.querySelectorAll('.frame');
                frames.forEach(frame => {{
                    const nodes = frame.dataset.nodes.split(',');
                    if (nodes.includes(node)) {{
                        frame.style.display = 'block';
                        frame.style.opacity = '1';
                    }} else {{
                        frame.style.opacity = '0.3';
                    }}
                }});
            }}
            
            // Auto-scroll animation
            let scrollSpeed = 0.5;
            function autoScroll() {{
                window.scrollBy(0, scrollSpeed);
                requestAnimationFrame(autoScroll);
            }}
            
            // Start auto-scroll after 3 seconds
            setTimeout(() => {{
                autoScroll();
            }}, 3000);
            
            // Add keyboard navigation
            document.addEventListener('keydown', function(e) {{
                switch(e.key) {{
                    case 'ArrowUp':
                        window.scrollBy(0, -100);
                        break;
                    case 'ArrowDown':
                        window.scrollBy(0, 100);
                        break;
                    case 'Home':
                        window.scrollTo(0, 0);
                        break;
                    case 'End':
                        window.scrollTo(0, document.body.scrollHeight);
                        break;
                }}
            }});
            
            // Build testing checklist functionality
            function updateChecklist(checkbox) {{
                const label = checkbox.nextElementSibling;
                if (checkbox.checked) {{
                    label.parentElement.classList.add('completed');
                    // Auto-check next item after a short delay
                    setTimeout(() => {{
                        const nextCheckbox = checkbox.parentElement.nextElementSibling?.querySelector('input[type="checkbox"]');
                        if (nextCheckbox && !nextCheckbox.checked) {{
                            nextCheckbox.checked = true;
                            updateChecklist(nextCheckbox);
                        }}
                    }}, 500);
                }} else {{
                    label.parentElement.classList.remove('completed');
                }}
            }}
            
            // Auto-check first item when page loads
            window.addEventListener('load', function() {{
                const firstCheckbox = document.getElementById('check1');
                if (firstCheckbox) {{
                    firstCheckbox.checked = true;
                    updateChecklist(firstCheckbox);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return make_response(html_content)

@app.route('/authenticated')
def authenticated_page():
    """
    Display the authenticated user page after successful login.
    This prevents form resubmission issues by using GET instead of POST.
    """
    # Check if user is authenticated
    if not session.get('authenticated', False):
        return redirect('/', code=302)
    
    # Get authentication data from session
    auth_data = session.get('auth_data', {})
    if not auth_data:
        return redirect('/', code=302)
    
    # Create the authenticated page HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yourl.Cloud Inc. - Authenticated Access</title>
        <meta name="description" content="Welcome to Yourl.Cloud Inc. - Your trusted cloud infrastructure and API services partner.">
        <meta name="robots" content="noindex, nofollow">
        
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-top: 20px;
                margin-bottom: 20px;
            }}
            .header {{ 
                text-align: center; 
                padding: 40px 0;
                border-bottom: 3px solid #667eea;
                margin-bottom: 30px;
            }}
            .logo {{ 
                font-size: 3rem; 
                font-weight: bold; 
                color: #667eea;
                margin-bottom: 10px;
            }}
            .tagline {{ 
                font-size: 1.2rem; 
                color: #666;
                margin-bottom: 20px;
            }}
            .success-banner {{ 
                background: linear-gradient(45deg, #28a745, #20c997);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }}
            .visitor-info {{ 
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                border-left: 5px solid #667eea;
            }}
            .experience-level {{
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .new-user {{ background: #28a745; color: white; }}
            .returning-user {{ background: #ffc107; color: #333; }}
            .returning-visitor {{ background: #17a2b8; color: white; }}
            
            .company-info {{ 
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-bottom: 30px;
            }}
            .info-card {{ 
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-top: 4px solid #667eea;
            }}
            .info-card h3 {{ 
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.3rem;
            }}
            .services {{ 
                background: #f8f9fa;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .services h2 {{ 
                color: #667eea;
                margin-bottom: 20px;
                text-align: center;
            }}
            .service-grid {{ 
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }}
            .service-item {{ 
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .service-item h4 {{ 
                color: #667eea;
                margin-bottom: 10px;
            }}
            .navigation {{ 
                text-align: center;
                margin-top: 30px;
                padding-top: 30px;
                border-top: 2px solid #eee;
            }}
            .nav-btn {{ 
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 25px;
                margin: 10px;
                transition: all 0.3s ease;
                font-weight: bold;
            }}
            .nav-btn:hover {{ 
                background: #5a6fd8;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .footer {{ 
                text-align: center;
                padding: 30px 0;
                color: #666;
                border-top: 2px solid #eee;
                margin-top: 30px;
            }}
            .privilege-badge {{
                display: inline-block;
                background: #ff6b6b;
                color: white;
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 0.8rem;
                margin: 5px;
            }}
            .affiliation-section {{
                background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            @media (max-width: 768px) {{
                .container {{ margin: 10px; padding: 15px; }}
                .logo {{ font-size: 2rem; }}
                .company-info {{ grid-template-columns: 1fr; }}
                .service-grid {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header with Company Identity -->
            <div class="header">
                <div class="logo">Yourl.Cloud Inc.</div>
                <div class="tagline">Secure Cloud Infrastructure & API Services</div>
                <p>United States • Global Operations • Enterprise Solutions</p>
            </div>

            <!-- Success Banner for Authenticated Users -->
            <div class="success-banner">
                <h2>🎉 Welcome to Yourl.Cloud Inc.</h2>
                <p><strong>Authentication Successful</strong> - You now have access to our enhanced services.</p>
                <p>Experience Level: <span class="experience-level {auth_data.get('experience_level', 'new_user')}">{auth_data.get('experience_level', 'new_user').replace('_', ' ').title()}</span></p>
            </div>

            <!-- Visitor Information Section -->
            <div class="visitor-info">
                <h3>👤 Your Visitor Profile</h3>
                <p><strong>Visitor ID:</strong> {auth_data.get('visitor_data', {}).get('visitor_id', 'Unknown')}</p>
                <p><strong>Total Visits:</strong> {auth_data.get('visitor_data', {}).get('total_visits', 1)}</p>
                <p><strong>Status:</strong> {'New Visitor' if auth_data.get('visitor_data', {}).get('is_new_visitor', True) else 'Returning Visitor'}</p>
                <p><strong>Code Usage:</strong> {'Has used access codes' if auth_data.get('visitor_data', {}).get('has_used_code', False) else 'First time using codes'}</p>
                {f'<p><strong>Tracking Key:</strong> {auth_data.get("visitor_data", {}).get("tracking_key")}</p>' if auth_data.get('visitor_data', {}).get('tracking_key') else ''}
            </div>

            <!-- Company Information for SEO -->
            <div class="company-info">
                <div class="info-card">
                    <h3>🏢 About Yourl.Cloud Inc.</h3>
                    <p>Yourl.Cloud Inc. is a leading technology company specializing in cloud infrastructure, API services, and digital solutions. Based in the United States, we serve clients globally with secure, scalable, and innovative technology solutions.</p>
                    <p><strong>Founded:</strong> 2024</p>
                    <p><strong>Headquarters:</strong> United States</p>
                    <p><strong>Industry:</strong> Cloud Computing, API Services, Digital Infrastructure</p>
                </div>
                
                <div class="info-card">
                    <h3>🌐 Global Operations</h3>
                    <p>Operating from the United States, Yourl.Cloud Inc. provides services to clients worldwide. Our infrastructure spans multiple regions, ensuring reliable, low-latency access to our services.</p>
                    <p><strong>Primary Region:</strong> US-West1 (Google Cloud)</p>
                    <p><strong>Service Availability:</strong> 24/7 Global Access</p>
                    <p><strong>Compliance:</strong> US-based data centers</p>
                </div>
                
                <div class="info-card">
                    <h3>🔒 Security & Compliance</h3>
                    <p>Yourl.Cloud Inc. maintains the highest standards of security and compliance. Our infrastructure is built on Google Cloud Platform, ensuring enterprise-grade security, reliability, and performance.</p>
                    <p><strong>Infrastructure:</strong> Google Cloud Platform</p>
                    <p><strong>Security:</strong> Enterprise-grade encryption</p>
                    <p><strong>Compliance:</strong> Industry-standard protocols</p>
                </div>
            </div>

            <!-- Services Section -->
            <div class="services">
                <h2>🚀 Our Services</h2>
                <div class="service-grid">
                    <div class="service-item">
                        <h4>☁️ Cloud Infrastructure</h4>
                        <p>Scalable, secure cloud solutions built on Google Cloud Platform with enterprise-grade reliability and performance.</p>
                    </div>
                    <div class="service-item">
                        <h4>🔌 API Services</h4>
                        <p>RESTful APIs and microservices architecture designed for modern applications and seamless integration.</p>
                    </div>
                    <div class="service-item">
                        <h4>🛡️ Security Solutions</h4>
                        <p>Advanced security protocols, encryption, and compliance measures to protect your data and applications.</p>
                    </div>
                    <div class="service-item">
                        <h4>📱 Digital Solutions</h4>
                        <p>Custom digital solutions tailored to your business needs, from web applications to mobile solutions.</p>
                    </div>
                </div>
            </div>

            <!-- Navigation Section -->
            <div class="navigation">
                <a href="/" class="nav-btn">🏠 Back to Landing Page</a>
                <a href="/api" class="nav-btn">🔌 API Documentation</a>
                <a href="/status" class="nav-btn">📊 Service Status</a>
                <a href="/data" class="nav-btn">📡 Data Stream</a>
            </div>

            <!-- Footer -->
            <div class="footer">
                <p>&copy; 2024 Yourl.Cloud Inc. All rights reserved. | United States | Global Operations</p>
                <p>Built with ❤️ for secure, scalable cloud solutions</p>
            </div>
        </div>
        
        <script>
            // Add some interactive elements
            document.querySelectorAll('.nav-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {{
                        this.style.transform = 'scale(1)';
                    }}, 150);
                }});
            }});
            
            // Add smooth scrolling for better UX
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{
                            behavior: 'smooth',
                            block: 'start'
                        }});
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    return make_response(html_content)

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors by returning the request URL.
    Compatible with Cloud Run domain mappings.
    """
    return jsonify({
        "error": "Not Found",
        "url": request.url,
        "message": "The requested resource was not found, but here's your request URL",
        "timestamp": datetime.utcnow().isoformat(),
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"],
        "cloud_run": {
            "original_host": get_original_host(),
            "original_protocol": get_original_protocol()
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors.
    """
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal Server Error",
        "url": request.url,
        "message": "An internal server error occurred",
        "timestamp": datetime.utcnow().isoformat(),
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"]
    }), 500

def launch_browser(url, delay=1.5):
    """
    Launch the default browser to the specified URL after a short delay.
    This allows the server to start up before the browser tries to connect.
    """
    def _launch():
        time.sleep(delay)  # Wait for server to start
        try:
            webbrowser.open(url)
            print(f"🌐 Browser launched: {url}")
        except Exception as e:
            print(f"⚠️ Could not launch browser: {e}")
    
    # Launch browser in a separate thread to avoid blocking
    browser_thread = threading.Thread(target=_launch, daemon=True)
    browser_thread.start()

def start_production_server():
    """
    Start the application using a production WSGI server.
    Enhanced for Cloud Run domain mapping compatibility.
    """
    print("🚀 Starting production WSGI server...")
    
    if platform.system() == "Windows":
        # Use Waitress on Windows
        try:
            import waitress
            print("✅ Using Waitress WSGI server (Windows)")
            # Suppress Waitress logging messages
            import logging
            logging.getLogger('waitress').setLevel(logging.ERROR)
            
            # Start Waitress server in a separate thread to allow custom output
            import threading
            def run_waitress():
                waitress.serve(app, host=HOST, port=PORT, threads=4, connection_limit=1000)
            
            server_thread = threading.Thread(target=run_waitress, daemon=True)
            server_thread.start()
            
            # Show user-friendly localhost URL
            display_host = 'localhost' if HOST == '0.0.0.0' else HOST
            print(f"🌐 Server running at: http://{display_host}:{PORT}")
            print("🚀 Yourl.Cloud is now accessible locally!")
            print("=" * 60)
            
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                return
        except ImportError:
            print("❌ Waitress not found. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "waitress"], check=True)
                import waitress
                print("✅ Waitress installed - starting production server...")
                # Suppress Waitress logging messages
                import logging
                logging.getLogger('waitress').setLevel(logging.ERROR)
                
                # Start Waitress server in a separate thread to allow custom output
                import threading
                def run_waitress():
                    waitress.serve(app, host=HOST, port=PORT, threads=4, connection_limit=1000)
                
                server_thread = threading.Thread(target=run_waitress, daemon=True)
                server_thread.start()
                
                # Show user-friendly localhost URL
                display_host = 'localhost' if HOST == '0.0.0.0' else HOST
                print(f"🌐 Server running at: http://{display_host}:{PORT}")
                print("🚀 Yourl.Cloud is now accessible locally!")
                print("=" * 60)
                
                # Keep main thread alive
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 Shutting down server...")
                    return
            except Exception as e:
                print(f"❌ Failed to install/use Waitress: {e}")
                print("🔄 Falling back to Flask development server...")
                app.run(host=HOST, port=PORT, debug=False, threaded=True)
    else:
        # Use Gunicorn on Unix-like systems
        try:
            import gunicorn
            print("✅ Using Gunicorn WSGI server (Unix)")
            cmd = ["gunicorn", "--bind", f"{HOST}:{PORT}", "--workers", "4", "app:app"]
            subprocess.run(cmd, check=True)
        except ImportError:
            print("❌ Gunicorn not found. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "gunicorn"], check=True)
                import gunicorn
                print("✅ Gunicorn installed - starting production server...")
                cmd = ["gunicorn", "--bind", f"{HOST}:{PORT}", "--workers", "4", "app:app"]
                subprocess.run(cmd, check=True)
            except Exception as e:
                print(f"❌ Failed to install/use Gunicorn: {e}")
                print("🔄 Falling back to Flask development server...")
                app.run(host=HOST, port=PORT, debug=False, threaded=True)

def attempt_code_recovery(visitor_id: str, user_agent: str, ip_address: str) -> dict:
    """
    Attempt to recover user experience based on their usage patterns.
    This respects privacy by using only stored behavioral data.
    """
    try:
        database_connection = os.environ.get('DATABASE_CONNECTION_STRING')
        if not database_connection:
            # Fallback: suggest current live code when database is not available
            current_code = get_current_marketing_code()
            return {
                'success': True,
                'message': f'Database not connected - using current live code: {current_code}',
                'suggested_code': current_code,
                'recovery_method': 'current_code_fallback',
                'usage_pattern': {
                    'total_attempts': 0,
                    'successful_attempts': 0,
                    'last_successful': None,
                    'last_attempt': None
                }
            }
        
        from scripts.database_client import DatabaseClient
        db_client = DatabaseClient(database_connection)
        
        # Get visitor's access history
        visitor_history = db_client.get_visitor_access_history(visitor_id)
        
        if not visitor_history:
            # No history found - suggest current code
            current_code = get_current_marketing_code()
            return {
                'success': True,
                'message': f'No previous usage history found - using current live code: {current_code}',
                'suggested_code': current_code,
                'recovery_method': 'current_code_no_history',
                'usage_pattern': {
                    'total_attempts': 0,
                    'successful_attempts': 0,
                    'last_successful': None,
                    'last_attempt': None
                }
            }
        
        # Analyze patterns to suggest recovery
        successful_codes = [h['access_code'] for h in visitor_history if h.get('success')]
        recent_codes = [h['access_code'] for h in visitor_history[-5:]]  # Last 5 attempts
        
        if successful_codes:
            # User has successfully used codes before - suggest the most recent successful one
            suggested_code = successful_codes[-1]
            recovery_method = 'previous_success'
            message = f"Based on your previous successful usage, try: {suggested_code}"
        elif recent_codes:
            # User has attempted codes recently - suggest the most recent attempt
            suggested_code = recent_codes[-1]
            recovery_method = 'recent_attempt'
            message = f"Based on your recent activity, you may have tried: {suggested_code}"
        else:
            # No clear pattern - suggest current code
            suggested_code = get_current_marketing_code()
            recovery_method = 'current_code'
            message = f"Using current live code: {suggested_code}"
        
        return {
            'success': True,
            'message': message,
            'suggested_code': suggested_code,
            'recovery_method': recovery_method,
            'usage_pattern': {
                'total_attempts': len(visitor_history),
                'successful_attempts': len(successful_codes),
                'last_successful': successful_codes[-1] if successful_codes else None,
                'last_attempt': recent_codes[-1] if recent_codes else None
            }
        }
        
    except Exception as e:
        print(f"⚠️ Error in code recovery: {e}")
        # Fallback: suggest current code on any error
        current_code = get_current_marketing_code()
        return {
            'success': True,
            'message': f'Recovery system error - using current live code: {current_code}',
            'suggested_code': current_code,
            'recovery_method': 'current_code_error_fallback'
        }

@app.route('/recover', methods=['GET', 'POST'])
def code_recovery() -> Response:
    """
    Code recovery endpoint for users who forgot their codes.
    Respects privacy by using only stored behavioral data.
    """
    if request.method == 'GET':
        # Show recovery form
        if os.path.exists('templates/recovery.html'):
            return make_response(render_template('recovery.html'))
        else:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Code Recovery - Yourl.Cloud</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #333; text-align: center; }}
                    .form-group {{ margin: 20px 0; }}
                    label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                    input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }}
                    button {{ background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                    button:hover {{ background: #0056b3; }}
                    .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .recovery-message {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .privacy-note {{ background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 20px 0; font-size: 14px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔐 Code Recovery</h1>
                    <div class="info">
                        <strong>Forgot your Yourl code?</strong><br>
                        Don't worry! We can help you recover your experience based on your previous usage patterns.
                    </div>
                    
                    <form method="POST">
                        <div class="form-group">
                            <label for="recovery_method">Recovery Method:</label>
                            <select name="recovery_method" id="recovery_method" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px;">
                                <option value="auto">🤖 Automatic Recovery (Recommended)</option>
                                <option value="manual">✍️ Manual Recovery</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="visitor_id">Visitor ID (if you remember it):</label>
                            <input type="text" id="visitor_id" name="visitor_id" placeholder="Leave blank for automatic detection">
                        </div>
                        
                        <button type="submit">🔍 Recover My Experience</button>
                    </form>
                    
                    <div class="privacy-note">
                        <strong>🔒 Privacy First:</strong> This recovery system uses only your stored behavioral data (codes you've used before, visit patterns) to help you regain access. We take safeguarding this data as seriously as PHI/PII.
                    </div>
                    
                    <div class="info">
                        <strong>Need Help?</strong><br>
                        <a href="/">← Back to Home</a> | <a href="/data">📊 Data Stream</a>
                    </div>
                </div>
            </body>
            </html>
            """
            return make_response(html_content)
    
    elif request.method == 'POST':
        # Handle recovery request
        recovery_method = request.form.get('recovery_method', 'auto')
        visitor_id = request.form.get('visitor_id', '').strip()
        
        # Get visitor ID from cookie if not provided
        if not visitor_id:
            visitor_id = request.cookies.get('visitor_id')
        
        if not visitor_id:
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Recovery Failed - Yourl.Cloud</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #333; text-align: center; }}
                    .error {{ background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #721c24; }}
                    .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔐 Recovery Failed</h1>
                    <div class="error">
                        <strong>No visitor ID found.</strong><br>
                        We couldn't identify your previous visits. This could happen if:
                        <ul>
                            <li>You're using a different browser or device</li>
                            <li>Your browser cookies were cleared</li>
                            <li>This is your first visit</li>
                        </ul>
                    </div>
                    
                    <div class="info">
                        <strong>What you can do:</strong><br>
                        • <a href="/">Try the current live code</a><br>
                        • <a href="/recover">Try recovery again</a><br>
                        • Contact support if you need assistance
                    </div>
                </div>
            </body>
            </html>
            """
            return make_response(error_html)
        
        # Attempt recovery
        recovery_result = attempt_code_recovery(
            visitor_id=visitor_id,
            user_agent=request.headers.get('User-Agent', ''),
            ip_address=get_client_ip() or ''
        )
        
        if recovery_result['success']:
            suggested_code = recovery_result['suggested_code']
            recovery_method_used = recovery_result['recovery_method']
            usage_pattern = recovery_result.get('usage_pattern', {})
            
            success_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Recovery Successful - Yourl.Cloud</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #333; text-align: center; }}
                    .success {{ background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #155724; }}
                    .code-display {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center; font-weight: bold; font-size: 18px; }}
                    .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .usage-stats {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    button {{ background: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 5px; }}
                    button:hover {{ background: #0056b3; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎉 Recovery Successful!</h1>
                    <div class="success">
                        <strong>We found your experience!</strong><br>
                        {recovery_result['message']}
                    </div>
                    
                    <div class="code-display">
                        <strong>Suggested Code:</strong><br>
                        <span style="font-size: 24px; color: #007bff;">{suggested_code}</span>
                    </div>
                    
                    <div class="usage-stats">
                        <strong>📊 Your Usage Pattern:</strong><br>
                        • Total attempts: {usage_pattern.get('total_attempts', 0)}<br>
                        • Successful attempts: {usage_pattern.get('successful_attempts', 0)}<br>
                        • Last successful: {usage_pattern.get('last_successful', 'None')}<br>
                        • Recovery method: {recovery_method_used.replace('_', ' ').title()}
                    </div>
                    
                    <div style="text-align: center;">
                        <button onclick="window.location.href='/'">🏠 Go to Home</button>
                        <button onclick="copyToClipboard('{suggested_code}')">📋 Copy Code</button>
                    </div>
                    
                    <div class="info">
                        <strong>Next Steps:</strong><br>
                        1. Copy the suggested code above<br>
                        2. Go to the <a href="/">home page</a><br>
                        3. Paste the code in the access field<br>
                        4. Enjoy your recovered experience!
                    </div>
                </div>
                
                <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        alert('Code copied to clipboard!');
                    }}, function(err) {{
                        console.error('Could not copy text: ', err);
                    }});
                }}
                </script>
            </body>
            </html>
            """
            return make_response(success_html)
        else:
            # Recovery failed
            failed_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Recovery Failed - Yourl.Cloud</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #333; text-align: center; }}
                    .error {{ background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0; color: #721c24; }}
                    .info {{ background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔐 Recovery Failed</h1>
                    <div class="error">
                        <strong>Recovery unsuccessful.</strong><br>
                        {recovery_result['message']}
                    </div>
                    
                    <div class="info">
                        <strong>What you can do:</strong><br>
                        • <a href="/">Try the current live code</a><br>
                        • <a href="/recover">Try recovery again</a><br>
                        • Contact support if you need assistance<br>
                        • Remember: It's OK to start over - the system will remember you based on how you use it!
                    </div>
                </div>
            </body>
            </html>
            """
            return make_response(failed_html)
    
    # Default return for any other method
    return make_response("Method not allowed", 405)

if __name__ == '__main__':
    # Determine the display address for users
    if HOST == '0.0.0.0':
        display_host = 'localhost'  # More user-friendly than 0.0.0.0
    else:
        display_host = HOST
    
    # Get current marketing code
    current_password = get_current_marketing_code()
    
    print(f"🚀 Starting URL API Server with Visual Inspection")
    print(f"📍 Host: {display_host}")
    print(f"🐛 Debug: {DEBUG}")
    print(f"🏭 Production: {PRODUCTION} (All instances are production instances)")
    print(f"🆔 Session: {FRIENDS_FAMILY_GUARD['session_id']}")
    print(f"🏢 Organization: {FRIENDS_FAMILY_GUARD['organization']}")
    print(f"🛡️ Friends and Family Guard: {'Enabled' if FRIENDS_FAMILY_GUARD['enabled'] else 'Disabled'}")
    print(f"👁️ Visual Inspection: PC/Phone/Tablet allowed, Watch blocked")
    print(f"☁️ Google Cloud Run Support: Enabled")
    print(f"🌐 Domain Mapping: {'Enabled' if CLOUD_RUN_CONFIG['domain_mapping_enabled'] else 'Disabled'}")
    print(f"🎪 Marketing Password: {current_password}")
    print("=" * 60)
    
    # Launch browser for local development (not for production/Cloud Run)
    if not os.environ.get('PORT'):
        local_url = f"http://{display_host}:{PORT}"
        print(f"🌐 Launching browser to: {local_url}")
        launch_browser(local_url)
    
    # Start with production WSGI server
    start_production_server()

