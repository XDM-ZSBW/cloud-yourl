#!/usr/bin/env python3
"""
Startup script for Yourl.Cloud Inc. API Server
==============================================

This script provides a convenient way to start the Yourl.Cloud Inc. API server
with proper configuration for both local development and production deployment.
Supports automatic port detection, browser launching, and production WSGI server.

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Environment: Production
WSGI Server: Gunicorn (Unix) / Waitress (Windows)
Domain Mapping: Compatible
Cloud Run Region: us-west1
"""

import os
import sys
import subprocess
import platform
from app import app, PRODUCTION, HOST, PORT, DEBUG

def start_production():
    """Start the application in production mode using appropriate WSGI server."""
    print("🚀 Starting in Production Mode (WSGI server)")
    print(f"📍 Host: {HOST}")
    print("🏭 Production: True (All instances are production instances)")
    print("=" * 50)
    
    # Check if we're on Windows
    if platform.system() == "Windows":
        print("🪟 Windows detected - using Waitress WSGI server")
        try:
            # Try to import waitress
            import waitress
            print("✅ Waitress found - starting production server...")
            
            # Start Waitress server in a separate thread to allow custom output
            import threading
            import time
            def run_waitress():
                waitress.serve(app, host=HOST, port=PORT)
            
            server_thread = threading.Thread(target=run_waitress, daemon=True)
            server_thread.start()
            
            # Show user-friendly localhost URL
            display_host = 'localhost' if HOST == '0.0.0.0' else HOST
            print(f"🌐 Server running at: http://{display_host}:{PORT}")
            print("🚀 Yourl.Cloud is now accessible locally!")
            print("=" * 50)
            
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
                
                # Start Waitress server in a separate thread to allow custom output
                import threading
                import time
                def run_waitress():
                    waitress.serve(app, host=HOST, port=PORT)
                
                server_thread = threading.Thread(target=run_waitress, daemon=True)
                server_thread.start()
                
                # Show user-friendly localhost URL
                display_host = 'localhost' if HOST == '0.0.0.0' else HOST
                print(f"🌐 Server running at: http://{display_host}:{PORT}")
                print("🚀 Yourl.Cloud is now accessible locally!")
                print("=" * 50)
                
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
                app.run(
                    host=HOST,
                    port=PORT,
                    debug=False,  # Always False in production
                    threaded=True
                )
    else:
        # Unix-like system - use Gunicorn
        print("🐧 Unix-like system detected - using Gunicorn WSGI server")
        cmd = [
            "gunicorn",
            "--config", "scripts/gunicorn.conf.py",
            "wsgi:app"
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start Gunicorn: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("❌ Gunicorn not found. Please install it with: pip install gunicorn")
            print("🔄 Falling back to Flask development server...")
            app.run(
                host=HOST,
                port=PORT,
                debug=False,  # Always False in production
                threaded=True
            )

def main():
    """Main entry point - all instances are production instances."""
    print("🚀 Yourl.Cloud Inc. API Server Startup")
    print("🏭 All instances deploy as production instances")
    print("👤 Tester decides: Personal use or Work use")
    print("=" * 50)
    
    # All instances are production instances
    start_production()

if __name__ == "__main__":
    main()
