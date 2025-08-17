#!/usr/bin/env python3
"""
Simple API Server with Visual Inspection and Google Cloud Run Support
===================================================================

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
import time

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

# Global password cache to ensure consistency
_current_password = None
_next_password = None

# App start time for uptime monitoring
_app_start_time = None

def generate_simple_password():
    """Generate a simple password for testing - cached for consistency"""
    global _current_password
    
    if _current_password is not None:
        return _current_password
    
    words = ["CLOUD", "FUTURE", "INNOVATE", "DREAM", "BUILD", "CREATE"]
    symbols = ["!", "@", "#", "$", "%", "&"]
    
    # Use environment variable or generate from timestamp
    fallback_id = os.environ.get('BUILD_ID', str(int(datetime.now().timestamp())))
    hash_num = int(hashlib.md5(fallback_id.encode()).hexdigest()[:8], 16)
    
    random.seed(hash_num)
    word = random.choice(words)
    symbol = random.choice(symbols)
    number = random.randint(10, 999)
    
    _current_password = f"{word}{number}{symbol}"
    return _current_password

def generate_next_password():
    """Generate the next password for authenticated users"""
    global _next_password
    
    if _next_password is not None:
        return _next_password
    
    words = ["ROCKET", "STAR", "MOON", "SUN", "OCEAN", "MOUNTAIN"]
    symbols = ["!", "@", "#", "$", "%", "&"]
    
    # Use a different seed for next password
    fallback_id = os.environ.get('BUILD_ID', str(int(datetime.now().timestamp()))) + "_next"
    hash_num = int(hashlib.md5(fallback_id.encode()).hexdigest()[:8], 16)
    
    random.seed(hash_num)
    word = random.choice(words)
    symbol = random.choice(symbols)
    number = random.randint(10, 999)
    
    _next_password = f"{word}{number}{symbol}"
    return _next_password

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

# Demo configuration for rapid prototyping
DEMO_CONFIG = {
    "password": generate_simple_password(),
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
        
        # Rich landing page content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Yourl.Cloud - URL API Server</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 0; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
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
                .form-section {{
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 10px;
                    margin: 30px 0;
                    text-align: center;
                }}
                .form-group {{ margin: 20px 0; }}
                label {{ 
                    display: block; 
                    margin-bottom: 10px; 
                    font-weight: bold; 
                    font-size: 1.1rem;
                    color: #333;
                }}
                input[type="text"], input[type="password"] {{ 
                    width: 100%; 
                    max-width: 400px;
                    padding: 15px; 
                    border: 2px solid #ddd; 
                    border-radius: 10px; 
                    font-size: 16px; 
                    text-align: center;
                    transition: border-color 0.3s ease;
                }}
                input[type="text"]:focus, input[type="password"]:focus {{ 
                    border-color: #667eea;
                    outline: none;
                }}
                button {{ 
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white; 
                    padding: 15px 40px; 
                    border: none; 
                    border-radius: 25px; 
                    cursor: pointer; 
                    font-size: 18px; 
                    font-weight: bold;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }}
                button:hover {{ 
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }}
                .password-display {{ 
                    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                    color: white;
                    padding: 20px; 
                    border-radius: 15px; 
                    margin: 30px 0; 
                    text-align: center; 
                    font-weight: bold;
                    font-size: 1.2rem;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .info {{ 
                    background: #e7f3ff; 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin: 20px 0; 
                    border-left: 5px solid #667eea;
                }}
                .connections-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }}
                .connection-card {{
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    border-top: 4px solid #667eea;
                    transition: transform 0.3s ease;
                }}
                .connection-card:hover {{
                    transform: translateY(-5px);
                }}
                .connection-card h3 {{
                    color: #667eea;
                    margin-bottom: 15px;
                    font-size: 1.3rem;
                }}
                .connection-card a {{
                    color: #667eea;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .connection-card a:hover {{
                    text-decoration: underline;
                }}
                .footer {{
                    text-align: center;
                    padding: 30px 0;
                    color: #666;
                    border-top: 2px solid #eee;
                    margin-top: 30px;
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    font-weight: bold;
                    text-transform: uppercase;
                    margin: 5px;
                }}
                .status-success {{ background: #d4edda; color: #155724; }}
                .status-info {{ background: #d1ecf1; color: #0c5460; }}
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

                <!-- Authentication Form Section -->
                <div class="form-section">
                    <h2>🚀 Launch Your Experience</h2>
                    <p>Enter the marketing password to access enhanced services and visual inspection capabilities.</p>
                    
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
                        <strong>🔒 Security Note:</strong> This password changes with each deployment to ensure security.<br>
                        <strong>🌐 Health Check:</strong> <a href="/health">/health</a> | 
                        <strong>📊 Status:</strong> <a href="/status">/status</a> |
                        <strong>🔌 API:</strong> <a href="/api">/api</a>
                    </div>
                </div>

                <!-- Company Information Section -->
                <div class="info">
                    <h3>🏢 About Yourl.Cloud Inc.</h3>
                    <p>Yourl.Cloud Inc. is a leading technology company specializing in cloud infrastructure, API services, and digital solutions. Based in the United States, we serve clients globally with secure, scalable, and innovative technology solutions.</p>
                    <p><strong>Founded:</strong> 2024 | <strong>Headquarters:</strong> United States | <strong>Industry:</strong> Cloud Computing, API Services, Digital Infrastructure</p>
                </div>

                <!-- Connections Grid -->
                <div class="connections-grid">
                    {''.join([f'''
                    <div class="connection-card">
                        <h3>{conn['name']}</h3>
                        <p>{conn['description']}</p>
                        <a href="{conn['url']}" target="_blank">🔗 Visit {conn['name']}</a>
                    </div>
                    ''' for conn in DEMO_CONFIG['connections']])}
                </div>

                <!-- Footer -->
                <div class="footer">
                    <p>&copy; 2024 Yourl.Cloud Inc. All rights reserved. | United States | Global Operations</p>
                    <p>Built with ❤️ for secure, scalable cloud solutions</p>
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
        next_password = generate_next_password()
        
        if password == current_password:
            session['authenticated'] = True
            session['last_access_code'] = current_password
            
            # Get current build version/commit hash
            try:
                import subprocess
                build_version = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                                     text=True, stderr=subprocess.DEVNULL).strip()[:8]
            except:
                build_version = "unknown"
            
            # Create JSON response with actual URL and personalized data
            json_response = {
                "status": "authenticated",
                "message": "🎉 Welcome to Yourl.Cloud!",
                "experience_level": "authenticated_user",
                "current_marketing_password": current_password,
                "next_marketing_password": next_password,
                "ownership": {
                    "perplexity": "current_marketing_password",
                    "cursor": "next_marketing_password"
                },
                "navigation": {
                    "back_to_landing": f"{get_original_protocol()}://{get_original_host()}/",
                    "api_endpoint": f"{get_original_protocol()}://{get_original_host()}/api",
                    "status_page": f"{get_original_protocol()}://{get_original_host()}/status"
                },
                "timestamp": datetime.utcnow().isoformat(),
                "organization": FRIENDS_FAMILY_GUARD["organization"],
                "build_version": build_version
            }
            
            return jsonify(json_response)
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

@app.route('/monitoring/health', methods=['GET'])
def monitoring_health():
    """Public health check endpoint for monitoring systems."""
    try:
        # Basic health checks
        global _app_start_time
        uptime = 'unknown'
        if _app_start_time:
            uptime = time.time() - _app_start_time
        
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'uptime': uptime,
            'version': 'yourl-cloud-2024',
            'environment': 'production' if PRODUCTION else 'development'
        }
        
        # Database health check
        database_connection = os.environ.get('DATABASE_CONNECTION_STRING')
        if database_connection:
            try:
                from scripts.database_client import DatabaseClient
                db_client = DatabaseClient(database_connection)
                # Simple ping test
                conn = db_client._get_connection()
                if conn:
                    conn.close()
                    health_status['database'] = 'connected'
                else:
                    health_status['database'] = 'disconnected'
                    health_status['status'] = 'degraded'
            except Exception as e:
                health_status['database'] = f'error: {str(e)}'
                health_status['status'] = 'degraded'
        else:
            health_status['database'] = 'not_configured'
        
        status_code = 200 if health_status['status'] == 'healthy' else 503
        
        return jsonify(health_status), status_code
        
    except Exception as e:
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/monitoring', methods=['GET'])
def monitoring_dashboard():
    """Monitoring dashboard for authenticated users."""
    # Check if user is authenticated
    if not session.get('authenticated', False):
        return jsonify({
            "error": "Access denied",
            "message": "Authentication required for monitoring access"
        }), 401
    
    return jsonify({
        "monitoring": {
            "status": "active",
            "endpoints": {
                "health": "/monitoring/health",
                "dashboard": "/monitoring"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    })

@app.route('/data', methods=['GET'])
def data_stream():
    """Enhanced data stream endpoint providing vertical linear datastream with horizontally scrollable wiki stories."""
    # Check if visitor has authenticated (used a valid code previously)
    if not session.get('authenticated', False):
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
                </div>
                <div>
                    <a href="/" class="nav-btn">🏠 Return to Landing Page</a>
                    <a href="/status" class="nav-btn">📊 Service Status</a>
                </div>
            </div>
        </body>
        </html>
        """, 403)
    
    # Generate dynamic story frames
    import time
    current_time = time.time()
    
    story_frames = [
        {
            "id": "frame_001",
            "timestamp": current_time - 3600,
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
            "timestamp": current_time - 1800,
            "title": "The Clipboard Bridge Phenomenon",
            "content": "At cb.yourl.cloud, we've created something extraordinary - a clipboard bridge that transcends physical boundaries. AI assistants can now share context seamlessly across family locations, creating a unified experience that feels like magic.",
            "category": "breakthrough_technology",
            "visual_elements": ["clipboard_bridge", "context_sharing", "seamless_experience"],
            "scroll_position": 100,
            "wiki_links": ["CLIPBOARD_BRIDGE_DEPLOYMENT.md", "ZAIDO_CLIPBOARD_RECOVERY_GUIDE.md"],
            "mind_map_nodes": ["clipboard", "bridge", "context", "unified"]
        }
    ]
    
    # Create the enhanced HTML response with vertical datastream
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
            .data-stream-title {{
                text-align: center;
                font-size: 2rem;
                margin-bottom: 30px;
                color: #00ff00;
                text-shadow: 0 0 20px #00ff00;
            }}
        </style>
    </head>
    <body>
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
                    {''.join(['<span class="visual-element">' + element.replace("_", " ").title() + '</span>' for element in frame['visual_elements']])}
                </div>
                <div class="wiki-links">
                    {''.join(['<a href="/knowledge-hub" class="wiki-link" target="_blank">📚 ' + link.replace(".md", "").replace("_", " ").title() + '</a>' for link in frame.get('wiki_links', [])])}
                </div>
            </div>
            ''' for frame in story_frames])}
        </div>
        
        <div class="navigation">
            <a href="/" class="nav-btn">🏠 Home</a>
            <a href="/api" class="nav-btn">🔌 API</a>
            <a href="/status" class="nav-btn">📊 Status</a>
            <a href="/data" class="nav-btn">📡 Data Stream</a>
            <a href="/knowledge-hub" class="nav-btn">🧠 Knowledge Hub</a>
        </div>
    </body>
    </html>
    """
    
    return make_response(html_content)

@app.route('/knowledge-hub', methods=['GET'])
def knowledge_hub():
    """Knowledge Hub endpoint providing access to wiki documentation."""
    # Check if user is authenticated
    if not session.get('authenticated', False):
        return jsonify({
            "error": "Access denied",
            "message": "Authentication required for knowledge hub access"
        }), 401
    
    # Create knowledge hub HTML
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Knowledge Hub - Yourl.Cloud Inc.</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                padding: 30px;
                margin-top: 20px;
            }
            .header { 
                text-align: center; 
                padding: 20px 0;
                border-bottom: 3px solid #667eea;
                margin-bottom: 30px;
            }
            .header h1 { 
                color: #667eea;
                margin-bottom: 10px;
            }
            .knowledge-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .knowledge-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-top: 4px solid #667eea;
                transition: transform 0.3s ease;
            }
            .knowledge-card:hover {
                transform: translateY(-5px);
            }
            .knowledge-card h3 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .knowledge-card p {
                color: #666;
                line-height: 1.6;
            }
            .navigation {
                text-align: center;
                margin-top: 30px;
                padding-top: 30px;
                border-top: 2px solid #eee;
            }
            .nav-btn {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 25px;
                margin: 10px;
                transition: all 0.3s ease;
                font-weight: bold;
            }
            .nav-btn:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Knowledge Hub</h1>
                <p>Yourl.Cloud Inc. - Comprehensive Documentation & Resources</p>
            </div>
            
            <div class="knowledge-grid">
                <div class="knowledge-card">
                    <h3>🏗️ Architecture Overview</h3>
                    <p>Comprehensive guide to the Yourl.Cloud system architecture, including cloud infrastructure, API design, and security protocols.</p>
                </div>
                
                <div class="knowledge-card">
                    <h3>🚀 Deployment Guide</h3>
                    <p>Step-by-step instructions for deploying Yourl.Cloud applications to Google Cloud Run with domain mapping support.</p>
                </div>
                
                <div class="knowledge-card">
                    <h3>🔒 Security Documentation</h3>
                    <p>Detailed security protocols, authentication methods, and best practices for maintaining secure cloud operations.</p>
                </div>
                
                <div class="knowledge-card">
                    <h3>📱 API Reference</h3>
                    <p>Complete API documentation including endpoints, authentication, request/response formats, and example usage.</p>
                </div>
                
                <div class="knowledge-card">
                    <h3>🛠️ Development Setup</h3>
                    <p>Local development environment setup, testing procedures, and contribution guidelines for developers.</p>
                </div>
                
                <div class="knowledge-card">
                    <h3>📊 Monitoring & Analytics</h3>
                    <p>System monitoring, health checks, performance metrics, and operational insights for production environments.</p>
                </div>
            </div>
            
            <div class="navigation">
                <a href="/" class="nav-btn">🏠 Back to Home</a>
                <a href="/data" class="nav-btn">📡 Data Stream</a>
                <a href="/api" class="nav-btn">🔌 API</a>
                <a href="/status" class="nav-btn">📊 Status</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return make_response(html_content)

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
    # Track app start time for uptime monitoring
    _app_start_time = time.time()
    
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
