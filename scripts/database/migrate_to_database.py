# Database Migration Script for Yourl.Cloud
# =========================================
#
# This script handles database migrations and schema updates
# for Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

class DatabaseMigration:
    """Database migration and schema update class."""
    
    def __init__(self, db_path: str = "yourl_cloud.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.migrations_table = "schema_migrations"
    
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
    
    def create_migrations_table(self) -> bool:
        """Create the migrations tracking table."""
        try:
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.migrations_table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    checksum TEXT,
                    execution_time REAL
                )
            ''')
            self.connection.commit()
            print(f"✅ Migrations table created: {self.migrations_table}")
            return True
        except Exception as e:
            print(f"❌ Failed to create migrations table: {e}")
            return False
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions."""
        try:
            self.cursor.execute(f"SELECT version FROM {self.migrations_table} ORDER BY version")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"⚠️ Could not get applied migrations: {e}")
            return []
    
    def record_migration(self, version: str, name: str, checksum: str = "", execution_time: float = 0.0) -> bool:
        """Record a migration as applied."""
        try:
            self.cursor.execute(f'''
                INSERT INTO {self.migrations_table} (version, name, checksum, execution_time)
                VALUES (?, ?, ?, ?)
            ''', (version, name, checksum, execution_time))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Failed to record migration: {e}")
            return False
    
    def apply_migration(self, version: str, name: str, sql_commands: List[str]) -> bool:
        """Apply a single migration."""
        start_time = datetime.now()
        
        try:
            print(f"🔄 Applying migration {version}: {name}")
            
            # Execute each SQL command
            for i, sql in enumerate(sql_commands):
                print(f"  Executing command {i+1}/{len(sql_commands)}")
                self.cursor.execute(sql)
            
            # Record the migration
            execution_time = (datetime.now() - start_time).total_seconds()
            if not self.record_migration(version, name, execution_time=execution_time):
                self.connection.rollback()
                return False
            
            self.connection.commit()
            print(f"✅ Migration {version} applied successfully")
            return True
            
        except Exception as e:
            print(f"❌ Migration {version} failed: {e}")
            self.connection.rollback()
            return False
    
    def get_pending_migrations(self) -> List[Dict[str, str]]:
        """Get list of pending migrations."""
        # Define available migrations
        available_migrations = [
            {
                'version': '001',
                'name': 'Add user preferences table',
                'sql': [
                    '''CREATE TABLE IF NOT EXISTS user_preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        preference_key TEXT NOT NULL,
                        preference_value TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        UNIQUE(user_id, preference_key)
                    )''',
                    'CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id)',
                    'CREATE INDEX IF NOT EXISTS idx_user_preferences_key ON user_preferences(preference_key)'
                ]
            },
            {
                'version': '002',
                'name': 'Add API keys table',
                'sql': [
                    '''CREATE TABLE IF NOT EXISTS api_keys (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        key_name TEXT NOT NULL,
                        api_key TEXT UNIQUE NOT NULL,
                        permissions TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_used DATETIME,
                        expires_at DATETIME,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )''',
                    'CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id)',
                    'CREATE INDEX IF NOT EXISTS idx_api_keys_key ON api_keys(api_key)'
                ]
            },
            {
                'version': '003',
                'name': 'Add notification settings table',
                'sql': [
                    '''CREATE TABLE IF NOT EXISTS notification_settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        notification_type TEXT NOT NULL,
                        email_enabled BOOLEAN DEFAULT 1,
                        push_enabled BOOLEAN DEFAULT 1,
                        frequency TEXT DEFAULT 'immediate',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        UNIQUE(user_id, notification_type)
                    )''',
                    'CREATE INDEX IF NOT EXISTS idx_notification_settings_user_id ON notification_settings(user_id)'
                ]
            }
        ]
        
        applied_versions = set(self.get_applied_migrations())
        pending = []
        
        for migration in available_migrations:
            if migration['version'] not in applied_versions:
                pending.append(migration)
        
        return pending
    
    def run_migrations(self) -> bool:
        """Run all pending migrations."""
        try:
            print("🚀 Starting database migrations...")
            
            # Ensure migrations table exists
            if not self.create_migrations_table():
                return False
            
            # Get pending migrations
            pending_migrations = self.get_pending_migrations()
            
            if not pending_migrations:
                print("✅ No pending migrations")
                return True
            
            print(f"📋 Found {len(pending_migrations)} pending migrations")
            
            # Apply each migration
            for migration in pending_migrations:
                if not self.apply_migration(
                    migration['version'],
                    migration['name'],
                    migration['sql']
                ):
                    return False
            
            print("✅ All migrations completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Migration process failed: {e}")
            return False
    
    def rollback_migration(self, version: str) -> bool:
        """Rollback a specific migration (if supported)."""
        print(f"⚠️ Rollback not implemented for migration {version}")
        return False
    
    def get_migration_status(self) -> Dict[str, Any]:
        """Get current migration status."""
        try:
            applied = self.get_applied_migrations()
            pending = self.get_pending_migrations()
            
            return {
                'applied_migrations': applied,
                'pending_migrations': len(pending),
                'total_migrations': len(applied) + len(pending),
                'database_path': self.db_path
            }
        except Exception as e:
            return {
                'error': f'Could not get migration status: {str(e)}'
            }

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration for Yourl.Cloud')
    parser.add_argument('action', choices=['migrate', 'status', 'rollback'],
                       help='Action to perform')
    parser.add_argument('--db-path', '-d', default='yourl_cloud.db', help='Database file path')
    parser.add_argument('--version', '-v', help='Migration version for rollback')
    
    args = parser.parse_args()
    
    migration = DatabaseMigration(args.db_path)
    
    try:
        if args.action == 'migrate':
            if migration.connect():
                success = migration.run_migrations()
                exit(0 if success else 1)
            else:
                exit(1)
                
        elif args.action == 'status':
            if migration.connect():
                status = migration.get_migration_status()
                print(json.dumps(status, indent=2))
                exit(0)
            else:
                exit(1)
                
        elif args.action == 'rollback':
            if not args.version:
                print("❌ Version required for rollback action")
                exit(1)
            
            if migration.connect():
                success = migration.rollback_migration(args.version)
                exit(0 if success else 1)
            else:
                exit(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
    finally:
        migration.disconnect()

if __name__ == "__main__":
    main()
