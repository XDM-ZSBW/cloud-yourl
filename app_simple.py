#!/usr/bin/env python3
"""
Simple Flask API Server with Wiki Visualization Dashboard
========================================================

A clean, working Flask application that provides a wiki visualization
dashboard for Yourl.Cloud's purpose and architecture.

Author: Yourl.Cloud Inc.
"""

from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Configuration
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 8080))

@app.route('/')
def home():
    """Landing page with marketing code input and current build code display"""
    
    # Generate a simple token code for demonstration
    import hashlib
    import time
    import random
    
    # Simple, friendly words for token codes
    friendly_words = [
        "CLOUD", "DREAM", "BUILD", "CREATE", "LAUNCH", "SPARK", "SHINE", "RISE", 
        "POWER", "MAGIC", "WONDER", "ROCKET", "STAR", "OCEAN", "MOUNTAIN", "FOREST",
        "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "TRIBE", "CLAN", "SQUAD"
    ]
    
    # Special characters
    special_chars = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
    
    # Generate deterministic but friendly token code
    current_time = int(time.time() // 3600)  # Change every hour
    random.seed(current_time)  # Use time as seed for consistency
    
    word = random.choice(friendly_words)
    number = random.randint(10, 99)  # Two digit number
    special = random.choice(special_chars)
    
    token_code = f"{word}{number}{special}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Yourl.Cloud - AI-Friendly Service Hub</title>
        <style>
            :root {{
                --primary-color: #667eea;
                --secondary-color: #764ba2;
                --accent-color: #ffd700;
                --text-primary: #333;
                --text-secondary: #666;
                --bg-primary: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                --bg-secondary: rgba(255, 255, 255, 0.95);
                --bg-tertiary: rgba(255, 255, 255, 0.9);
                --border-radius: 20px;
                --shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: var(--bg-primary);
                color: var(--text-primary);
                min-height: 100vh;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 3rem;
                animation: fadeInUp 0.8s ease-out;
            }}
            
            .header h1 {{
                font-size: clamp(2rem, 5vw, 3.5rem);
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .header p {{
                font-size: clamp(1rem, 2.5vw, 1.3rem);
                opacity: 0.9;
                max-width: 600px;
                margin: 0 auto;
            }}
            
            .main-panel {{
                background: var(--bg-secondary);
                border-radius: var(--border-radius);
                backdrop-filter: blur(10px);
                box-shadow: var(--shadow);
                padding: 2rem;
                margin-bottom: 2rem;
                animation: fadeInUp 0.8s ease-out 0.2s both;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .input-section {{
                margin-bottom: 2rem;
            }}
            
            .input-section h2 {{
                margin-bottom: 1rem;
                color: var(--primary-color);
                font-size: 1.5rem;
                text-align: center;
            }}
            
            .input-group {{
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
                flex-wrap: wrap;
            }}
            
            .input-group input {{
                flex: 1;
                min-width: 250px;
                padding: 1rem;
                border: 2px solid #ddd;
                border-radius: 10px;
                background: white;
                color: var(--text-primary);
                font-size: 1rem;
                transition: var(--transition);
                font-family: 'Courier New', monospace;
                letter-spacing: 1px;
                text-align: center;
            }}
            
            .input-group input:focus {{
                outline: none;
                border-color: var(--accent-color);
                box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3);
            }}
            
            .input-group input:not(:placeholder-shown) {{
                border-color: var(--primary-color);
                background: rgba(255, 255, 255, 0.98);
            }}
            
            .input-hint {{
                text-align: center;
                margin-top: 0.5rem;
                opacity: 0.8;
            }}
            
            .input-hint small {{
                font-size: 0.9rem;
                color: var(--text-secondary);
            }}
            
            .submit-btn {{
                background: var(--primary-color);
                border: none;
                color: white;
                padding: 1rem 2rem;
                border-radius: 10px;
                cursor: pointer;
                font-size: 1.1rem;
                transition: var(--transition);
                white-space: nowrap;
            }}
            
            .submit-btn:hover {{
                background: var(--secondary-color);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}
            
            .token-code-display {{
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(236, 240, 241, 0.9) 100%);
                border-radius: 15px;
                padding: 1.5rem;
                margin-bottom: 2rem;
                text-align: center;
                border: 2px solid #3498db;
                box-shadow: 0 8px 25px rgba(52, 152, 219, 0.15);
                backdrop-filter: blur(10px);
            }}
            
            .token-code-display h2 {{
                color: #2c3e50;
                margin-bottom: 1rem;
                font-size: 1.3rem;
                font-weight: 600;
            }}
            
            .code-display {{
                font-family: 'Courier New', monospace;
                font-size: clamp(1.2rem, 3vw, 1.8rem);
                font-weight: bold;
                color: #2c3e50;
                background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%);
                padding: 1.5rem;
                border-radius: 12px;
                margin: 1rem 0;
                cursor: pointer;
                border: 3px solid #3498db;
                transition: var(--transition);
                text-align: center;
                letter-spacing: 2px;
                box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
                position: relative;
                overflow: hidden;
            }}
            
            .code-display:hover {{
                background: linear-gradient(135deg, #d5dbdb 0%, #a4a4a4 100%);
                border-color: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
            }}
            
            .code-display:active {{
                transform: translateY(0);
                box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
            }}
            
            .copy-feedback {{
                display: none;
                color: #27ae60;
                font-weight: bold;
                margin-top: 0.5rem;
                animation: fadeIn 0.3s ease-in;
                background: rgba(39, 174, 96, 0.1);
                padding: 0.5rem 1rem;
                border-radius: 8px;
                border: 1px solid rgba(39, 174, 96, 0.3);
            }}
            
            .code-hint {{
                font-style: italic;
                opacity: 0.9;
                font-size: 0.9rem;
                margin-top: 0.5rem;
                color: #34495e;
                background: rgba(52, 73, 94, 0.05);
                padding: 0.5rem;
                border-radius: 6px;
                border-left: 3px solid #3498db;
            }}
            
            .previous-codes {{
                background: var(--bg-tertiary);
                border-radius: 15px;
                padding: 1.5rem;
                margin-bottom: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.2);
                animation: fadeInUp 0.8s ease-out 0.3s both;
            }}
            
            .previous-codes h2 {{
                color: var(--primary-color);
                margin-bottom: 0.5rem;
                font-size: 1.3rem;
                text-align: center;
            }}
            
            .no-codes {{
                text-align: center;
                padding: 2rem 1rem;
                opacity: 0.8;
            }}
            
            .no-codes p {{
                margin-bottom: 0.5rem;
                font-size: 1rem;
            }}
            
            .no-codes-hint {{
                font-size: 0.9rem;
                opacity: 0.7;
                font-style: italic;
            }}
            
            .nav-links {{
                margin-top: 2rem;
                text-align: center;
            }}
            
            .nav-links a {{
                display: inline-block;
                margin: 10px;
                padding: 10px 20px;
                background: var(--bg-tertiary);
                color: var(--primary-color);
                text-decoration: none;
                border-radius: 8px;
                transition: var(--transition);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .nav-links a:hover {{
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}
            
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            

            
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 1rem;
                }}
                
                .input-group {{
                    flex-direction: column;
                }}
                
                .input-group input {{
                    min-width: auto;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header Section -->
            <header class="header">
                <h1>Yourl.Cloud</h1>
                <p>AI-Friendly Service Hub - Professional cloud solutions and AI services</p>
            </header>

            <!-- Main Authentication Panel -->
            <main class="main-panel">
                <div class="input-section">
                    <h2>🔐 Access Your Services</h2>
                    <form method="POST" action="/">
                        <div class="input-group">
                            <input 
                                type="text" 
                                name="password" 
                                placeholder="Enter your token code" 
                                required
                                aria-label="Token code"
                                autocomplete="off"
                            >
                            <button type="submit" class="submit-btn">
                                🚀 Launch
                            </button>
                        </div>
                        <div class="input-hint">
                            <small>💡 Token codes look like: WORD + two digits + special character (e.g., CLOUD42!, DREAM15@)</small>
                        </div>
                    </form>
                </div>

                <!-- Token Code Display -->
                <div class="token-code-display">
                    <h2>🎯 Current Token Code</h2>
                    <div class="code-display" id="codeText" onclick="copyTokenCode()" role="button" tabindex="0" aria-label="Click to copy current token code">
                        {token_code}
                    </div>
                    <div class="copy-feedback" id="copyFeedback">✅ Token code copied to clipboard!</div>
                    <div class="code-hint">💡 Click the token code above to copy it to your clipboard</div>
                </div>

                <!-- Previous Codes Section -->
                <div class="previous-codes">
                                    <h2>📚 Your Previous Token Codes</h2>
                <div class="no-codes">
                    <p>🎯 No previous token codes yet - this will be your first time!</p>
                    <p class="no-codes-hint">Successfully use the current token code above to start building your history.</p>
                </div>
                </div>
            </main>

            <div class="nav-links">
                <a href="/data">📊 Data Dashboard</a>
                <a href="/status">📈 Status</a>
                <a href="/health">❤️ Health</a>
            </div>
        </div>

        <script>
            // Copy token code functionality
            function copyTokenCode() {{
                const codeText = document.getElementById('codeText');
                const copyFeedback = document.getElementById('copyFeedback');
                
                if (navigator.clipboard && window.isSecureContext) {{
                    // Use modern clipboard API
                    navigator.clipboard.writeText(codeText.textContent.trim()).then(() => {{
                        showCopyFeedback();
                    }}).catch(err => {{
                        console.error('Failed to copy: ', err);
                        fallbackCopy();
                    }});
                }} else {{
                    // Fallback for older browsers
                    fallbackCopy();
                }}
            }}
            
            function fallbackCopy() {{
                const codeText = document.getElementById('codeText');
                const textArea = document.createElement('textarea');
                textArea.value = codeText.textContent.trim();
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                textArea.style.top = '-999999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                
                try {{
                    const successful = document.execCommand('copy');
                    if (successful) {{
                        showCopyFeedback();
                    }}
                }} catch (err) {{
                    console.error('Fallback copy failed: ', err);
                }}
                
                document.body.removeChild(textArea);
            }}
            
            function showCopyFeedback() {{
                const copyFeedback = document.getElementById('copyFeedback');
                copyFeedback.style.display = 'block';
                
                setTimeout(() => {{
                    copyFeedback.style.display = 'none';
                }}, 2000);
            }}
            
            // Add keyboard navigation for token code display
            document.getElementById('codeText').addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' || e.key === ' ') {{
                    e.preventDefault();
                    copyTokenCode();
                }}
            }});
            
            // Add real-time input feedback
            const passwordInput = document.querySelector('input[name="password"]');
            if (passwordInput) {{
                passwordInput.addEventListener('input', function() {{
                    const value = this.value.trim();
                    if (value.length > 0) {{
                        this.style.borderColor = value.length >= 8 ? 'var(--accent-color)' : 'var(--primary-color)';
                    }} else {{
                        this.style.borderColor = '#ddd';
                    }}
                }});
                
                // Show entered text clearly
                passwordInput.addEventListener('focus', function() {{
                    this.style.fontSize = '1.1rem';
                    this.style.fontWeight = 'bold';
                }});
                
                passwordInput.addEventListener('blur', function() {{
                    this.style.fontSize = '1rem';
                    this.style.fontWeight = 'normal';
                }});
            }}
        </script>
    </body>
    </html>
    """
    return make_response(html_content)

@app.route('/', methods=['POST'])
def authenticate():
    """Handle authentication and redirect to data dashboard"""
    password = request.form.get('password', '')
    
    # Generate the same token code that was shown on the landing page
    import hashlib
    import time
    import random
    
    # Simple, friendly words for token codes
    friendly_words = [
        "CLOUD", "DREAM", "BUILD", "CREATE", "LAUNCH", "SPARK", "SHINE", "RISE", 
        "POWER", "MAGIC", "WONDER", "ROCKET", "STAR", "OCEAN", "MOUNTAIN", "FOREST",
        "FRIEND", "FAMILY", "TEAM", "SQUAD", "CREW", "TRIBE", "CLAN", "SQUAD"
    ]
    
    # Special characters
    special_chars = ["!", "@", "#", "$", "%", "&", "*", "+", "=", "?", "~", "^"]
    
    # Generate deterministic but friendly token code
    current_time = int(time.time() // 3600)  # Change every hour
    random.seed(current_time)  # Use time as seed for consistency
    
    word = random.choice(friendly_words)
    number = random.randint(10, 99)  # Two digit number
    special = random.choice(special_chars)
    
    current_token_code = f"{word}{number}{special}"
    
    # Check against the current token code
    if password.strip() == current_token_code:
        return make_response("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/data">
            <title>Redirecting...</title>
        </head>
        <body>
            <p>Authentication successful! Redirecting to dashboard...</p>
            <script>window.location.href = '/data';</script>
        </body>
        </html>
        """)
    else:
        return make_response(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="3; url=/">
            <title>Access Denied</title>
        </head>
        <body>
            <p>Invalid code: "{password}"</p>
            <p>Expected: "{current_token_code}"</p>
            <p>Redirecting back to login...</p>
            <script>setTimeout(() => window.location.href = '/', 3000);</script>
        </body>
        </html>
        """)

@app.route('/data')
def data_stream():
    """Wiki Visualization Dashboard - Interactive exploration of Yourl.Cloud's purpose and architecture"""
    
    # Create comprehensive wiki sections that represent the project's purpose
    wiki_sections = [
        {
            "id": "1",
            "title": "Project Overview",
            "description": "Core mission and vision of Yourl.Cloud",
            "content": "Yourl.Cloud is a production-ready Python Flask API designed for trust-based AI systems. The platform provides advanced features including Cloud Run domain mapping compatibility, Friends and Family Guard security rulesets, visual inspection capabilities, and production WSGI server support.",
            "category": "overview",
            "status": "featured",
            "lastUpdate": datetime.now() - timedelta(minutes=5),
            "links": ["Architecture Overview", "Security Features", "Technology Stack"]
        },
        {
            "id": "2",
            "title": "Architecture Overview",
            "description": "Complete system architecture and design",
            "content": "The system is built with Python Flask 3.0.2, WSGI servers (Gunicorn/Waitress), Google Cloud Run deployment, and comprehensive security layers including authentication, authorization, encryption, and audit trails.",
            "category": "architecture",
            "status": "active",
            "lastUpdate": datetime.now() - timedelta(minutes=3),
            "links": ["Technology Stack", "Security Architecture", "Deployment Guide"]
        },
        {
            "id": "3",
            "title": "Security Features",
            "description": "Friends and Family Guard security ruleset",
            "content": "Implements comprehensive security with device-based access control, multi-factor authentication, role-based authorization, complete audit logging, and compliance with GDPR, SOC 2, and ISO 27001 standards.",
            "category": "security",
            "status": "active",
            "lastUpdate": datetime.now() - timedelta(minutes=2),
            "links": ["Security Checklist", "Access Control", "Audit & Compliance"]
        },
        {
            "id": "4",
            "title": "Development Workflow",
            "description": "Development process and best practices",
            "content": "Comprehensive development workflow including local development setup, testing procedures, code standards, CI/CD pipeline, and deployment processes with automated testing and security scanning.",
            "category": "development",
            "status": "active",
            "lastUpdate": datetime.now() - timedelta(minutes=4),
            "links": ["Technology Stack", "Deployment Guide", "Testing Procedures"]
        },
        {
            "id": "5",
            "title": "Cloud Run Deployment",
            "description": "Production deployment on Google Cloud",
            "content": "Full Cloud Run compatibility with automatic scaling, domain mapping, load balancing, health monitoring, and disaster recovery with 99.9% uptime target and cross-region failover capabilities.",
            "category": "deployment",
            "status": "active",
            "lastUpdate": datetime.now() - timedelta(minutes=1),
            "links": ["Architecture Overview", "Infrastructure Setup", "Performance Metrics"]
        },
        {
            "id": "6",
            "title": "Knowledge Hub",
            "description": "Central documentation and learning center",
            "content": "Comprehensive knowledge transfer hub serving as the central navigation point for all aspects of the solution, including interactive features, search capabilities, and continuous improvement processes.",
            "category": "overview",
            "status": "featured",
            "lastUpdate": datetime.now() - timedelta(minutes=6),
            "links": ["Wiki System", "Documentation", "Learning Paths"]
        }
    ]
    
    def get_category_icon(category):
        """Helper function to get category icons"""
        icons = {
            'overview': '🎯',
            'architecture': '🏗️',
            'security': '🔐',
            'development': '🚀',
            'deployment': '🌐'
        }
        return icons.get(category, '📚')
    
    # Create the HTML response with wiki visualization
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wiki Visualization Dashboard - Yourl.Cloud Inc.</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            .header h1 {{
                font-size: 3rem;
                color: #667eea;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header p {{
                font-size: 1.3rem;
                color: #666;
                margin-bottom: 30px;
            }}
            .project-info {{
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
            }}
            .project-info h2 {{
                font-size: 2rem;
                margin-bottom: 15px;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .metric-card {{
                background: rgba(255, 255, 255, 0.95);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }}
            .metric-card:hover {{
                transform: translateY(-5px);
            }}
            .metric-number {{
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .metric-label {{
                color: #666;
                font-size: 0.9rem;
            }}
            .category-filters {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}
            .filter-btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                background: rgba(255, 255, 255, 0.9);
                color: #667eea;
            }}
            .filter-btn.active {{
                background: #667eea;
                color: white;
                transform: scale(1.05);
            }}
            .filter-btn:hover {{
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }}
            .wiki-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 25px;
                margin-bottom: 30px;
            }}
            .wiki-card {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                cursor: pointer;
                border-left: 5px solid #667eea;
            }}
            .wiki-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
            }}
            .card-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            .card-title {{
                font-size: 1.3rem;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }}
            .card-description {{
                color: #666;
                line-height: 1.6;
                margin-bottom: 15px;
            }}
            .card-content {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                display: none;
            }}
            .card-content.show {{
                display: block;
            }}
            .card-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }}
            .link-tag {{
                background: #e3f2fd;
                color: #1976d2;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: 500;
            }}
            .status-badge {{
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: capitalize;
            }}
            .status-featured {{ background: #e8f5e8; color: #2e7d32; }}
            .status-active {{ background: #e3f2fd; color: #1976d2; }}
            .status-updated {{ background: #fff3e0; color: #f57c00; }}
            .status-planned {{ background: #fce4ec; color: #c2185b; }}
            .category-icon {{
                font-size: 1.5rem;
                margin-right: 10px;
            }}
            .knowledge-flow {{
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            .flow-steps {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }}
            .flow-step {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            .flow-icon {{
                font-size: 2.5rem;
                margin-bottom: 15px;
            }}
            .purpose-summary {{
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            .purpose-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }}
            .purpose-card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                border-top: 5px solid #667eea;
            }}
            .purpose-icon {{
                font-size: 3rem;
                margin-bottom: 15px;
            }}
            .footer {{
                text-align: center;
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }}
            .status-badges {{
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
                margin: 20px 0;
            }}
            .status-badge-large {{
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 1rem;
                font-weight: 600;
                text-transform: uppercase;
            }}
            .status-success {{ background: #e8f5e8; color: #2e7d32; }}
            .status-info {{ background: #e3f2fd; color: #1976d2; }}
            .status-warning {{ background: #fff3e0; color: #f57c00; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Wiki Visualization Dashboard</h1>
                <p>Interactive exploration of Yourl.Cloud's purpose and architecture</p>
                <div class="project-info">
                    <h2>Yourl.Cloud</h2>
                    <p>Trust-Based AI Platform for Families Worldwide</p>
                </div>
            </div>

            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-number">{len(wiki_sections)}</div>
                    <div class="metric-label">Wiki Sections</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{len([s for s in wiki_sections if s['status'] == 'active'])}</div>
                    <div class="metric-label">Active Sections</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{len([s for s in wiki_sections if s['status'] == 'featured'])}</div>
                    <div class="metric-label">Featured Content</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{len([s for s in wiki_sections if s['status'] == 'planned'])}</div>
                    <div class="metric-label">Future Features</div>
                </div>
            </div>

            <div class="category-filters">
                <button class="filter-btn active" onclick="filterByCategory('all')">🌟 All Categories</button>
                <button class="filter-btn" onclick="filterByCategory('overview')">🎯 Overview</button>
                <button class="filter-btn" onclick="filterByCategory('architecture')">🏗️ Architecture</button>
                <button class="filter-btn" onclick="filterByCategory('security')">🔐 Security</button>
                <button class="filter-btn" onclick="filterByCategory('development')">🚀 Development</button>
                <button class="filter-btn" onclick="filterByCategory('deployment')">🌐 Deployment</button>
            </div>

            <div class="wiki-grid">
                {''.join([f'''
                <div class="wiki-card" data-category="{section['category']}" onclick="toggleContent(this)">
                    <div class="card-header">
                        <div>
                            <span class="category-icon">{get_category_icon(section['category'])}</span>
                            <div class="card-title">{section['title']}</div>
                        </div>
                        <span class="status-badge status-{section['status']}">{section['status']}</span>
                    </div>
                    <div class="card-description">{section['description']}</div>
                    <div class="card-content" id="content-{section['id']}">
                        <p><strong>Content:</strong></p>
                        <p>{section['content']}</p>
                        <p><strong>Related Links:</strong></p>
                        <div class="card-links">
                            {''.join([f'<span class="link-tag">{link}</span>' for link in section['links']])}
                        </div>
                    </div>
                    <div class="card-links">
                        {''.join([f'<span class="link-tag">{link}</span>' for link in section['links']])}
                    </div>
                    <div style="margin-top: 15px; font-size: 0.8rem; color: #999;">
                        Last updated: {section['lastUpdate'].strftime('%H:%M:%S')} | Category: {section['category']}
                    </div>
                </div>
                ''' for section in wiki_sections])}
            </div>

            <div class="knowledge-flow">
                <h2>🧠 Knowledge Flow Architecture</h2>
                <p>This visualization represents how Yourl.Cloud's wiki system flows from raw information to actionable knowledge</p>
                <div class="flow-steps">
                    <div class="flow-step">
                        <div class="flow-icon">📚</div>
                        <h4>Documentation</h4>
                    </div>
                    <div class="flow-step">
                        <div class="flow-icon">🔍</div>
                        <h4>Discovery</h4>
                    </div>
                    <div class="flow-step">
                        <div class="flow-icon">💡</div>
                        <h4>Insights</h4>
                    </div>
                    <div class="flow-step">
                        <div class="flow-icon">🚀</div>
                        <h4>Action</h4>
                    </div>
                </div>
            </div>

            <div class="purpose-summary">
                <h2>🎯 Project Purpose & Mission</h2>
                <div class="purpose-grid">
                    <div class="purpose-card">
                        <div class="purpose-icon">🤝</div>
                        <h4>Trust-Based AI</h4>
                        <p>Building AI systems that families can trust and rely on</p>
                    </div>
                    <div class="purpose-card">
                        <div class="purpose-icon">🌍</div>
                        <h4>Global Family Platform</h4>
                        <p>Serving families worldwide with secure, reliable technology</p>
                    </div>
                    <div class="purpose-card">
                        <div class="purpose-icon">🔒</div>
                        <h4>Security First</h4>
                        <p>Implementing enterprise-grade security for family protection</p>
                    </div>
                </div>
            </div>

            <div class="footer">
                <h3>📊 Wiki Status</h3>
                <div class="status-badges">
                    <span class="status-badge-large status-success">Knowledge Stream Active</span>
                    <span class="status-badge-large status-info">Interactive Learning</span>
                    <span class="status-badge-large status-warning">Continuous Updates</span>
                </div>
                <p style="margin-top: 20px; color: #666;">
                    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </div>

        <script>
            function filterByCategory(category) {{
                // Update active filter button
                document.querySelectorAll('.filter-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                event.target.classList.add('active');
                
                // Filter wiki cards
                const cards = document.querySelectorAll('.wiki-card');
                cards.forEach(card => {{
                    if (category === 'all' || card.dataset.category === category) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }}
            
            function toggleContent(card) {{
                const contentId = card.querySelector('.card-content').id;
                const content = document.getElementById(contentId);
                content.classList.toggle('show');
            }}
            
            // Add some interactive effects
            document.querySelectorAll('.wiki-card').forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px)';
                }});
                
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0)';
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    return make_response(html_content)

@app.route('/status')
def status():
    """Service status endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Yourl.Cloud Wiki Visualization",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "uptime": "running",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"🚀 Starting Yourl.Cloud Wiki Visualization Server...")
    print(f"🌐 Server will be available at: http://localhost:{PORT}")
    print(f"📊 Wiki Dashboard: http://localhost:{PORT}/data")
    print(f"🏠 Landing Page: http://localhost:{PORT}/")
    app.run(host=HOST, port=PORT, debug=True)
