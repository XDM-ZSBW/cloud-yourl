# Service Code Manager for Yourl.Cloud
# ===================================
#
# This script provides service code management for Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import json
import secrets
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

class ServiceCodeManager:
    """Service code management class."""
    
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
        """Ensure service code tables exist."""
        try:
            # Service codes table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    service_name TEXT NOT NULL,
                    description TEXT,
                    permissions TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME
                )
            ''')
            
            # Service usage log
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_usage_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_id INTEGER NOT NULL,
                    service_name TEXT NOT NULL,
                    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (code_id) REFERENCES service_codes (id)
                )
            ''')
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def generate_code(self, length: int = 12) -> str:
        """Generate a unique service code."""
        while True:
            # Generate alphanumeric code
            code = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))
            
            # Check if code already exists
            if not self.code_exists(code):
                return code
    
    def code_exists(self, code: str) -> bool:
        """Check if a service code already exists."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM service_codes WHERE code = ?", (code,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Exception:
            return False
    
    def create_code(self, service_name: str, description: str = "", 
                   permissions: str = "", valid_days: int = 365) -> Optional[str]:
        """Create a new service code."""
        try:
            code = self.generate_code()
            expires_at = datetime.now() + timedelta(days=valid_days) if valid_days > 0 else None
            
            self.cursor.execute('''
                INSERT INTO service_codes (code, service_name, description, permissions, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (code, service_name, description, permissions, expires_at))
            
            self.connection.commit()
            print(f"✅ Created service code: {code}")
            return code
            
        except Exception as e:
            print(f"❌ Failed to create service code: {e}")
            self.connection.rollback()
            return None
    
    def get_code_info(self, code: str) -> Optional[Dict[str, Any]]:
        """Get information about a service code."""
        try:
            self.cursor.execute('''
                SELECT id, code, service_name, description, permissions,
                       is_active, created_at, expires_at
                FROM service_codes WHERE code = ?
            ''', (code,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'code': row[1],
                    'service_name': row[2],
                    'description': row[3],
                    'permissions': row[4],
                    'is_active': bool(row[5]),
                    'created_at': row[6],
                    'expires_at': row[7]
                }
            return None
            
        except Exception as e:
            print(f"❌ Failed to get code info: {e}")
            return None
    
    def is_code_valid(self, code: str, service_name: str = None) -> Dict[str, Any]:
        """Check if a service code is valid for use."""
        code_info = self.get_code_info(code)
        if not code_info:
            return {'valid': False, 'reason': 'Code not found'}
        
        if not code_info['is_active']:
            return {'valid': False, 'reason': 'Code is inactive'}
        
        if service_name and code_info['service_name'] != service_name:
            return {'valid': False, 'reason': 'Code not valid for this service'}
        
        if code_info['expires_at'] and datetime.fromisoformat(code_info['expires_at']) < datetime.now():
            return {'valid': False, 'reason': 'Code has expired'}
        
        return {'valid': True, 'code_info': code_info}
    
    def use_code(self, code: str, service_name: str, 
                ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
        """Use a service code."""
        validation = self.is_code_valid(code, service_name)
        if not validation['valid']:
            return validation
        
        code_info = validation['code_info']
        
        try:
            # Log usage
            self.cursor.execute('''
                INSERT INTO service_usage_log (code_id, service_name, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ''', (code_info['id'], service_name, ip_address, user_agent))
            
            self.connection.commit()
            
            return {
                'valid': True,
                'code': code,
                'service_name': code_info['service_name'],
                'permissions': code_info['permissions'],
                'description': code_info['description'],
                'message': 'Service code used successfully'
            }
            
        except Exception as e:
            print(f"❌ Failed to use service code: {e}")
            self.connection.rollback()
            return {'valid': False, 'reason': 'Database error'}
    
    def get_all_codes(self, service_name: Optional[str] = None, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all service codes."""
        try:
            query = '''
                SELECT id, code, service_name, description, permissions,
                       is_active, created_at, expires_at
                FROM service_codes
            '''
            params = []
            
            conditions = []
            if service_name:
                conditions.append("service_name = ?")
                params.append(service_name)
            
            if active_only:
                conditions.append("is_active = 1")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY created_at DESC"
            
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            codes = []
            for row in rows:
                codes.append({
                    'id': row[0],
                    'code': row[1],
                    'service_name': row[2],
                    'description': row[3],
                    'permissions': row[4],
                    'is_active': bool(row[5]),
                    'created_at': row[6],
                    'expires_at': row[7]
                })
            
            return codes
            
        except Exception as e:
            print(f"❌ Failed to get codes: {e}")
            return []
    
    def update_code(self, code: str, **kwargs) -> bool:
        """Update a service code."""
        try:
            allowed_fields = ['description', 'permissions', 'is_active', 'expires_at']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = ?")
                    values.append(value)
            
            if not updates:
                return False
            
            values.append(code)
            query = f"UPDATE service_codes SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE code = ?"
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            print(f"✅ Updated service code: {code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update code: {e}")
            self.connection.rollback()
            return False
    
    def delete_code(self, code: str) -> bool:
        """Delete a service code."""
        try:
            self.cursor.execute("DELETE FROM service_codes WHERE code = ?", (code,))
            self.connection.commit()
            
            print(f"✅ Deleted service code: {code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete code: {e}")
            self.connection.rollback()
            return False
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get service code usage statistics."""
        try:
            # Total codes
            self.cursor.execute("SELECT COUNT(*) FROM service_codes")
            total_codes = self.cursor.fetchone()[0]
            
            # Active codes
            self.cursor.execute("SELECT COUNT(*) FROM service_codes WHERE is_active = 1")
            active_codes = self.cursor.fetchone()[0]
            
            # Codes by service
            self.cursor.execute('''
                SELECT service_name, COUNT(*) as count
                FROM service_codes
                GROUP BY service_name
                ORDER BY count DESC
            ''')
            service_counts = [{'service': row[0], 'count': row[1]} for row in self.cursor.fetchall()]
            
            # Recent usage
            self.cursor.execute('''
                SELECT COUNT(*) FROM service_usage_log
                WHERE used_at >= datetime('now', '-24 hours')
            ''')
            recent_usage = self.cursor.fetchone()[0]
            
            return {
                'total_codes': total_codes,
                'active_codes': active_codes,
                'service_counts': service_counts,
                'recent_usage_24h': recent_usage
            }
            
        except Exception as e:
            print(f"❌ Failed to get statistics: {e}")
            return {}

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Service Code Manager for Yourl.Cloud')
    parser.add_argument('action', choices=['create', 'list', 'info', 'use', 'update', 'delete', 'stats'],
                       help='Action to perform')
    parser.add_argument('--code', '-c', help='Service code')
    parser.add_argument('--service', '-s', help='Service name')
    parser.add_argument('--description', '-d', help='Code description')
    parser.add_argument('--permissions', '-p', help='Code permissions')
    parser.add_argument('--valid-days', '-v', type=int, help='Valid days')
    parser.add_argument('--db-path', '-b', default='yourl_cloud.db', help='Database file path')
    
    args = parser.parse_args()
    
    manager = ServiceCodeManager(args.db_path)
    
    try:
        if not manager.connect():
            exit(1)
        
        manager.ensure_tables_exist()
        
        if args.action == 'create':
            if not args.service:
                print("❌ Service name required for create action")
                exit(1)
            
            code = manager.create_code(
                service_name=args.service,
                description=args.description or "",
                permissions=args.permissions or "",
                valid_days=args.valid_days or 365
            )
            
            if code:
                print(f"✅ Created service code: {code}")
            else:
                exit(1)
                
        elif args.action == 'list':
            codes = manager.get_all_codes(service_name=args.service)
            print(f"📋 Found {len(codes)} service codes:")
            for code_info in codes:
                print(f"  {code_info['code']}: {code_info['service_name']} - {code_info['description']}")
                
        elif args.action == 'info':
            if not args.code:
                print("❌ Code required for info action")
                exit(1)
            
            info = manager.get_code_info(args.code)
            if info:
                print(json.dumps(info, indent=2, default=str))
            else:
                print("❌ Code not found")
                exit(1)
                
        elif args.action == 'use':
            if not args.code or not args.service:
                print("❌ Code and service required for use action")
                exit(1)
            
            result = manager.use_code(args.code, args.service)
            print(json.dumps(result, indent=2))
            
        elif args.action == 'stats':
            stats = manager.get_usage_statistics()
            print(json.dumps(stats, indent=2))
            
        elif args.action == 'update':
            if not args.code:
                print("❌ Code required for update action")
                exit(1)
            
            updates = {}
            if args.description:
                updates['description'] = args.description
            if args.permissions:
                updates['permissions'] = args.permissions
            
            if updates:
                success = manager.update_code(args.code, **updates)
                exit(0 if success else 1)
            else:
                print("❌ No updates specified")
                exit(1)
                
        elif args.action == 'delete':
            if not args.code:
                print("❌ Code required for delete action")
                exit(1)
            
            success = manager.delete_code(args.code)
            exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
    finally:
        manager.disconnect()

if __name__ == "__main__":
    main()
