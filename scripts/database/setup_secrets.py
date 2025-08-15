# Setup Secrets for Yourl.Cloud
# =============================
#
# This script sets up and manages secrets for Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import json
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

class SecretsManager:
    """Secrets management and setup class."""
    
    def __init__(self, db_path: str = "yourl_cloud.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Connect to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
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
    
    def ensure_tables_exist(self) -> bool:
        """Ensure secrets tables exist."""
        try:
            # Secrets table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS secrets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    secret_key TEXT UNIQUE NOT NULL,
                    secret_value TEXT NOT NULL,
                    description TEXT,
                    category TEXT DEFAULT 'general',
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME
                )
            ''')
            
            # Secret access log
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS secret_access_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    secret_id INTEGER NOT NULL,
                    accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    access_type TEXT DEFAULT 'read',
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (secret_id) REFERENCES secrets (id)
                )
            ''')
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def generate_secret(self, length: int = 32) -> str:
        """Generate a secure random secret."""
        return secrets.token_urlsafe(length)
    
    def hash_secret(self, secret: str) -> str:
        """Hash a secret value for storage."""
        return hashlib.sha256(secret.encode()).hexdigest()
    
    def create_secret(self, secret_key: str, secret_value: str, 
                     description: str = "", category: str = "general",
                     expires_days: Optional[int] = None) -> bool:
        """Create a new secret."""
        try:
            expires_at = None
            if expires_days:
                expires_at = datetime.now() + timedelta(days=expires_days)
            
            self.cursor.execute('''
                INSERT INTO secrets (secret_key, secret_value, description, category, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (secret_key, secret_value, description, category, expires_at))
            
            self.connection.commit()
            print(f"✅ Created secret: {secret_key}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create secret: {e}")
            self.connection.rollback()
            return False
    
    def get_secret(self, secret_key: str) -> Optional[str]:
        """Get a secret value."""
        try:
            self.cursor.execute('''
                SELECT secret_value, is_active, expires_at
                FROM secrets WHERE secret_key = ?
            ''', (secret_key,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
            
            secret_value, is_active, expires_at = row
            
            if not is_active:
                print(f"⚠️ Secret {secret_key} is inactive")
                return None
            
            if expires_at and datetime.fromisoformat(expires_at) < datetime.now():
                print(f"⚠️ Secret {secret_key} has expired")
                return None
            
            # Log access
            self.cursor.execute('''
                INSERT INTO secret_access_log (secret_id, access_type)
                SELECT id, 'read' FROM secrets WHERE secret_key = ?
            ''', (secret_key,))
            
            self.connection.commit()
            return secret_value
            
        except Exception as e:
            print(f"❌ Failed to get secret: {e}")
            return None
    
    def list_secrets(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all secrets."""
        try:
            query = '''
                SELECT secret_key, description, category, is_active, created_at, expires_at
                FROM secrets
            '''
            params = []
            
            if category:
                query += " WHERE category = ?"
                params.append(category)
            
            query += " ORDER BY created_at DESC"
            
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            secrets_list = []
            for row in rows:
                secrets_list.append({
                    'secret_key': row[0],
                    'description': row[1],
                    'category': row[2],
                    'is_active': bool(row[3]),
                    'created_at': row[4],
                    'expires_at': row[5]
                })
            
            return secrets_list
            
        except Exception as e:
            print(f"❌ Failed to list secrets: {e}")
            return []
    
    def update_secret(self, secret_key: str, **kwargs) -> bool:
        """Update a secret."""
        try:
            allowed_fields = ['secret_value', 'description', 'category', 'is_active', 'expires_at']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = ?")
                    values.append(value)
            
            if not updates:
                return False
            
            values.append(secret_key)
            query = f"UPDATE secrets SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE secret_key = ?"
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            print(f"✅ Updated secret: {secret_key}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update secret: {e}")
            self.connection.rollback()
            return False
    
    def delete_secret(self, secret_key: str) -> bool:
        """Delete a secret."""
        try:
            self.cursor.execute("DELETE FROM secrets WHERE secret_key = ?", (secret_key,))
            self.connection.commit()
            
            print(f"✅ Deleted secret: {secret_key}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete secret: {e}")
            self.connection.rollback()
            return False
    
    def setup_default_secrets(self) -> bool:
        """Set up default secrets for Yourl.Cloud."""
        try:
            print("🚀 Setting up default secrets...")
            
            default_secrets = [
                {
                    'key': 'JWT_SECRET',
                    'value': self.generate_secret(64),
                    'description': 'JWT signing secret for authentication',
                    'category': 'security'
                },
                {
                    'key': 'SESSION_SECRET',
                    'value': self.generate_secret(32),
                    'description': 'Session encryption secret',
                    'category': 'security'
                },
                {
                    'key': 'API_KEY_SECRET',
                    'value': self.generate_secret(48),
                    'description': 'API key generation secret',
                    'category': 'security'
                },
                {
                    'key': 'ENCRYPTION_KEY',
                    'value': self.generate_secret(32),
                    'description': 'Data encryption key',
                    'category': 'security'
                },
                {
                    'key': 'GOOGLE_CLOUD_PROJECT_ID',
                    'value': 'yourl-cloud',
                    'description': 'Google Cloud project ID',
                    'category': 'cloud'
                },
                {
                    'key': 'CLIPBOARD_BRIDGE_URL',
                    'value': 'https://cb.yourl.cloud',
                    'description': 'Clipboard bridge service URL',
                    'category': 'service'
                }
            ]
            
            for secret in default_secrets:
                if not self.create_secret(
                    secret['key'],
                    secret['value'],
                    secret['description'],
                    secret['category']
                ):
                    return False
            
            print("✅ Default secrets setup completed")
            return True
            
        except Exception as e:
            print(f"❌ Default secrets setup failed: {e}")
            return False
    
    def get_secret_statistics(self) -> Dict[str, Any]:
        """Get secrets usage statistics."""
        try:
            # Total secrets
            self.cursor.execute("SELECT COUNT(*) FROM secrets")
            total_secrets = self.cursor.fetchone()[0]
            
            # Active secrets
            self.cursor.execute("SELECT COUNT(*) FROM secrets WHERE is_active = 1")
            active_secrets = self.cursor.fetchone()[0]
            
            # Secrets by category
            self.cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM secrets
                GROUP BY category
                ORDER BY count DESC
            ''')
            category_counts = [{'category': row[0], 'count': row[1]} for row in self.cursor.fetchall()]
            
            # Recent access
            self.cursor.execute('''
                SELECT COUNT(*) FROM secret_access_log
                WHERE accessed_at >= datetime('now', '-24 hours')
            ''')
            recent_access = self.cursor.fetchone()[0]
            
            return {
                'total_secrets': total_secrets,
                'active_secrets': active_secrets,
                'category_counts': category_counts,
                'recent_access_24h': recent_access
            }
            
        except Exception as e:
            print(f"❌ Failed to get statistics: {e}")
            return {}

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Secrets Manager for Yourl.Cloud')
    parser.add_argument('action', choices=['setup', 'create', 'get', 'list', 'update', 'delete', 'stats'],
                       help='Action to perform')
    parser.add_argument('--key', '-k', help='Secret key')
    parser.add_argument('--value', '-v', help='Secret value')
    parser.add_argument('--description', '-d', help='Secret description')
    parser.add_argument('--category', '-c', help='Secret category')
    parser.add_argument('--db-path', '-b', default='yourl_cloud.db', help='Database file path')
    
    args = parser.parse_args()
    
    manager = SecretsManager(args.db_path)
    
    try:
        if not manager.connect():
            exit(1)
        
        manager.ensure_tables_exist()
        
        if args.action == 'setup':
            success = manager.setup_default_secrets()
            exit(0 if success else 1)
            
        elif args.action == 'create':
            if not args.key or not args.value:
                print("❌ Key and value required for create action")
                exit(1)
            
            success = manager.create_secret(
                args.key,
                args.value,
                args.description or "",
                args.category or "general"
            )
            exit(0 if success else 1)
            
        elif args.action == 'get':
            if not args.key:
                print("❌ Key required for get action")
                exit(1)
            
            value = manager.get_secret(args.key)
            if value:
                print(f"✅ Secret value: {value}")
            else:
                print("❌ Secret not found or inaccessible")
                exit(1)
                
        elif args.action == 'list':
            secrets = manager.list_secrets(args.category)
            print(f"📋 Found {len(secrets)} secrets:")
            for secret in secrets:
                print(f"  {secret['secret_key']}: {secret['description']} ({secret['category']})")
                
        elif args.action == 'stats':
            stats = manager.get_secret_statistics()
            print(json.dumps(stats, indent=2))
            
        elif args.action == 'update':
            if not args.key:
                print("❌ Key required for update action")
                exit(1)
            
            updates = {}
            if args.value:
                updates['secret_value'] = args.value
            if args.description:
                updates['description'] = args.description
            if args.category:
                updates['category'] = args.category
            
            if updates:
                success = manager.update_secret(args.key, **updates)
                exit(0 if success else 1)
            else:
                print("❌ No updates specified")
                exit(1)
                
        elif args.action == 'delete':
            if not args.key:
                print("❌ Key required for delete action")
                exit(1)
            
            success = manager.delete_secret(args.key)
            exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
    finally:
        manager.disconnect()

if __name__ == "__main__":
    main()
