#!/usr/bin/env python3
"""
Simple API Server with Visual Inspection and Google Cloud Run Support
====================================================================

A simplified Flask application for container deployment.
Enhanced for Google Cloud Run deployment with basic functionality.

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Google Cloud Run: Supported
WSGI Server: Production Ready
Domain Mapping: Compatible
"""

from flask import Flask, request, jsonify, render_template_string, make_response, session
import os
import logging
import platform
import random
import hashlib
from datetime import datetime

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
PORT = int(os.environ.get('PORT', 8080))

DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
PRODUCTION = True  # Always production for all deployments

# Cloud Run Domain Mapping Configuration
CLOUD_RUN_CONFIG = {
    "domain_mapping_enabled": True,
    "region": "us-west1",
    "trust_proxy": True,
    "cors_enabled": True,
    "health_check_path": "/health",
    "readiness_check_path": "/health"
}

def generate_simple_password():
    """Generate a simple password for testing"""
    words = ["CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE"]
    symbols = ["!", "@", "#", "$", "%", "&"]
    
    # Use environment variable or generate from timestamp
    fallback_id = os.environ.get('BUILD_ID', str(int(datetime.now().timestamp())))
    hash_num = int(hashlib.md5(fallback_id.encode()).hexdigest()[:8], 16)
    
    random.seed(hash_num)
    word = random.choice(words)
    symbol = random.choice(symbols)
    number = random.randint(10, 999)
    
    return f"{word}{number}{symbol}"

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

# Configure Flask for Cloud Run domain mapping compatibility
app.config.update(
    PREFERRED_URL_SCHEME='https',
    USE_X_SENDFILE=False,
    SERVER_NAME=None
)

def get_client_ip():
    """Get the real client IP address, handling Cloud Run's X-Forwarded headers."""
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.remote_addr

def get_original_host():
    """Get the original host from X-Forwarded-Host header."""
    return request.headers.get('X-Forwarded-Host', request.host)

def get_original_protocol():
    """Get the original protocol from X-Forwarded-Proto header."""
    return request.headers.get('X-Forwarded-Proto', 'https')

def detect_device_type(user_agent):
    """Detect device type based on User-Agent string."""
    ua_lower = user_agent.lower()
    
    if any(keyword in ua_lower for keyword in ['watch', 'wearable', 'smartwatch']):
        return 'watch'
    if any(keyword in ua_lower for keyword in ['mobile', 'android', 'iphone', 'phone']):
        return 'phone'
    if any(keyword in ua_lower for keyword in ['tablet', 'ipad']):
        return 'tablet'
    return 'pc'

def is_visual_inspection_allowed(device_type):
    """Check if visual inspection is allowed for the given device type."""
    if not FRIENDS_FAMILY_GUARD["enabled"]:
        return True
    return FRIENDS_FAMILY_GUARD["visual_inspection"].get(f"{device_type}_allowed", False)

@app.route('/', methods=['GET', 'POST'])
def main_endpoint():
    """Main endpoint that handles both GET (landing page) and POST (authentication)."""
    if request.method == 'GET':
        current_password = generate_simple_password()
        
        html_content = f"""
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
        """
        
        response = make_response(html_content)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    elif request.method == 'POST':
        password = request.form.get('password', '')
        current_password = generate_simple_password()
        
        if password == current_password:
            session['authenticated'] = True
            session['last_access_code'] = current_password
            
            return jsonify({
                "status": "authenticated",
                "message": "🎉 Welcome to Yourl.Cloud!",
                "current_marketing_password": current_password,
                "timestamp": datetime.utcnow().isoformat(),
                "organization": FRIENDS_FAMILY_GUARD["organization"]
            })
        else:
            return jsonify({
                "status": "failed",
                "message": "Invalid password. Please try again.",
                "current_marketing_password": current_password
            }), 401
    
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def get_request_url():
    """API endpoint that returns the request URL and metadata."""
    url = request.url
    method = request.method
    headers = dict(request.headers)
    user_agent = headers.get('User-Agent', 'Unknown')
    device_type = detect_device_type(user_agent)
    
    client_ip = get_client_ip()
    original_host = get_original_host()
    original_protocol = get_original_protocol()
    
    if is_visual_inspection_allowed(device_type):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Yourl.Cloud - Visual Inspection</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 2.5em; font-weight: 300; }}
                .content {{ padding: 30px; }}
                .url-display {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 10px; padding: 20px; margin: 20px 0; word-break: break-all; font-family: 'Courier New', monospace; font-size: 14px; }}
                .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
                .info-card {{ background: #f8f9fa; border-radius: 10px; padding: 20px; border-left: 4px solid #007bff; }}
                .info-card h3 {{ margin: 0 0 10px 0; color: #007bff; }}
                .status-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
                .status-success {{ background: #d4edda; color: #155724; }}
                .status-info {{ background: #d1ecf1; color: #0c5460; }}
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
                            <p><strong>Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
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
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    else:
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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run domain mapping compatibility."""
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
        "wsgi_server": "gunicorn",
        "production_mode": True,
        "deployment_model": "all_instances_production",
        "port": PORT,
        "host": get_original_host(),
        "protocol": get_original_protocol()
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with service information."""
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
        "wsgi_server": "gunicorn",
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

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by returning the request URL."""
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
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal Server Error",
        "url": request.url,
        "message": "An internal server error occurred",
        "timestamp": datetime.utcnow().isoformat(),
        "friends_family_guard": FRIENDS_FAMILY_GUARD["enabled"]
    }), 500

if __name__ == '__main__':
    print(f"🚀 Starting simplified URL API Server")
    print(f"📍 Host: {HOST}")
    print(f"🐛 Debug: {DEBUG}")
    print(f"🏭 Production: {PRODUCTION}")
    print(f"🆔 Session: {FRIENDS_FAMILY_GUARD['session_id']}")
    print(f"🏢 Organization: {FRIENDS_FAMILY_GUARD['organization']}")
    print(f"🛡️ Friends and Family Guard: {'Enabled' if FRIENDS_FAMILY_GUARD['enabled'] else 'Disabled'}")
    print(f"☁️ Google Cloud Run Support: Enabled")
    print(f"🌐 Domain Mapping: {'Enabled' if CLOUD_RUN_CONFIG['domain_mapping_enabled'] else 'Disabled'}")
    print("=" * 60)
    
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=True)
