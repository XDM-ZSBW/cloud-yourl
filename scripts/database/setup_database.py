# Database Setup Script for Yourl.Cloud
# =====================================
#
# This script sets up the initial database schema and tables
# for Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

class DatabaseSetup:
    """Database setup and initialization class."""
    
    def __init__(self, db_path: str = "yourl_cloud.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Connect to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print(f"✅ Connected to database: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✅ Database connection closed")
    
    def create_tables(self) -> bool:
        """Create all necessary tables."""
        try:
            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    role TEXT DEFAULT 'user'
                )
            ''')
            
            # Marketing codes table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS marketing_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    description TEXT,
                    discount_percent REAL DEFAULT 0.0,
                    max_uses INTEGER DEFAULT -1,
                    current_uses INTEGER DEFAULT 0,
                    valid_from DATETIME DEFAULT CURRENT_TIMESTAMP,
                    valid_until DATETIME,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Clipboard history table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS clipboard_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT NOT NULL,
                    content_hash TEXT UNIQUE,
                    tags TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    format TEXT DEFAULT 'text',
                    size INTEGER,
                    source TEXT DEFAULT 'web',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Sessions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME,
                    is_active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Audit log table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    table_name TEXT,
                    record_id INTEGER,
                    old_values TEXT,
                    new_values TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            self.connection.commit()
            print("✅ All tables created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            self.connection.rollback()
            return False
    
    def create_indexes(self) -> bool:
        """Create database indexes for better performance."""
        try:
            # Indexes for users table
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            
            # Indexes for marketing codes table
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_marketing_codes_code ON marketing_codes(code)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_marketing_codes_active ON marketing_codes(is_active)')
            
            # Indexes for clipboard history table
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_clipboard_user_id ON clipboard_history(user_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_clipboard_timestamp ON clipboard_history(timestamp)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_clipboard_content_hash ON clipboard_history(content_hash)')
            
            # Indexes for sessions table
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at)')
            
            # Indexes for audit log table
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_log(user_id)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)')
            self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action)')
            
            self.connection.commit()
            print("✅ All indexes created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create indexes: {e}")
            self.connection.rollback()
            return False
    
    def insert_sample_data(self) -> bool:
        """Insert sample data for testing."""
        try:
            # Sample user
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin@yourl.cloud', 'sample_hash', 'admin'))
            
            # Sample marketing codes
            sample_codes = [
                ('WELCOME10', 'Welcome discount 10%', 10.0, 100, 0),
                ('NEWUSER20', 'New user discount 20%', 20.0, 50, 0),
                ('SPECIAL15', 'Special offer 15%', 15.0, 200, 0)
            ]
            
            for code, desc, discount, max_uses, current_uses in sample_codes:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO marketing_codes (code, description, discount_percent, max_uses, current_uses)
                    VALUES (?, ?, ?, ?, ?)
                ''', (code, desc, discount, max_uses, current_uses))
            
            self.connection.commit()
            print("✅ Sample data inserted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to insert sample data: {e}")
            self.connection.rollback()
            return False
    
    def verify_setup(self) -> Dict[str, Any]:
        """Verify that the database setup is correct."""
        try:
            # Check if all tables exist
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.cursor.fetchall()]
            
            expected_tables = ['users', 'marketing_codes', 'clipboard_history', 'sessions', 'audit_log']
            missing_tables = [table for table in expected_tables if table not in tables]
            
            # Check table row counts
            table_counts = {}
            for table in expected_tables:
                if table in tables:
                    self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = self.cursor.fetchone()[0]
                    table_counts[table] = count
            
            # Check indexes
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
            indexes = [row[0] for row in self.cursor.fetchall()]
            
            return {
                'status': 'success' if not missing_tables else 'warning',
                'tables': {
                    'expected': expected_tables,
                    'found': tables,
                    'missing': missing_tables
                },
                'row_counts': table_counts,
                'indexes': indexes,
                'database_path': self.db_path
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Verification failed: {str(e)}'
            }
    
    def reset_database(self) -> bool:
        """Reset the database by dropping all tables."""
        try:
            # Get all table names
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.cursor.fetchall()]
            
            # Drop all tables
            for table in tables:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            
            self.connection.commit()
            print("✅ Database reset successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to reset database: {e}")
            self.connection.rollback()
            return False
    
    def setup_complete(self) -> bool:
        """Complete database setup process."""
        try:
            print("🚀 Starting database setup...")
            
            if not self.connect():
                return False
            
            # Create tables
            if not self.create_tables():
                return False
            
            # Create indexes
            if not self.create_indexes():
                return False
            
            # Insert sample data
            if not self.insert_sample_data():
                return False
            
            # Verify setup
            verification = self.verify_setup()
            print(f"📊 Setup verification: {verification['status']}")
            
            if verification['status'] == 'success':
                print("✅ Database setup completed successfully!")
                return True
            else:
                print("⚠️ Database setup completed with warnings")
                return True
                
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Setup for Yourl.Cloud')
    parser.add_argument('action', choices=['setup', 'verify', 'reset', 'create-tables', 'create-indexes'],
                       help='Action to perform')
    parser.add_argument('--db-path', '-d', default='yourl_cloud.db', help='Database file path')
    parser.add_argument('--sample-data', '-s', action='store_true', help='Include sample data')
    
    args = parser.parse_args()
    
    db_setup = DatabaseSetup(args.db_path)
    
    try:
        if args.action == 'setup':
            success = db_setup.setup_complete()
            exit(0 if success else 1)
            
        elif args.action == 'verify':
            if db_setup.connect():
                verification = db_setup.verify_setup()
                print(json.dumps(verification, indent=2))
                exit(0 if verification['status'] != 'error' else 1)
            else:
                exit(1)
                
        elif args.action == 'reset':
            if db_setup.connect():
                success = db_setup.reset_database()
                exit(0 if success else 1)
            else:
                exit(1)
                
        elif args.action == 'create-tables':
            if db_setup.connect():
                success = db_setup.create_tables()
                exit(0 if success else 1)
            else:
                exit(1)
                
        elif args.action == 'create-indexes':
            if db_setup.connect():
                success = db_setup.create_indexes()
                exit(0 if success else 1)
            else:
                exit(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
