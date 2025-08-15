# Marketing Code Manager for Yourl.Cloud
# =====================================
#
# This script provides high-level marketing code management
# for Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import json
import secrets
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

class MarketingCodeManager:
    """High-level marketing code management class."""
    
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
        """Ensure marketing code tables exist."""
        try:
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
            
            # Code usage log
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS code_usage_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_id INTEGER NOT NULL,
                    user_id INTEGER,
                    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (code_id) REFERENCES marketing_codes (id)
                )
            ''')
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def generate_code(self, length: int = 8) -> str:
        """Generate a unique marketing code."""
        while True:
            # Generate alphanumeric code
            code = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))
            
            # Check if code already exists
            if not self.code_exists(code):
                return code
    
    def code_exists(self, code: str) -> bool:
        """Check if a marketing code already exists."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM marketing_codes WHERE code = ?", (code,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Exception:
            return False
    
    def create_code(self, description: str, discount_percent: float = 0.0, 
                   max_uses: int = -1, valid_days: int = 30) -> Optional[str]:
        """Create a new marketing code."""
        try:
            code = self.generate_code()
            valid_until = datetime.now() + timedelta(days=valid_days) if valid_days > 0 else None
            
            self.cursor.execute('''
                INSERT INTO marketing_codes (code, description, discount_percent, max_uses, valid_until)
                VALUES (?, ?, ?, ?, ?)
            ''', (code, description, discount_percent, max_uses, valid_until))
            
            self.connection.commit()
            print(f"✅ Created marketing code: {code}")
            return code
            
        except Exception as e:
            print(f"❌ Failed to create marketing code: {e}")
            self.connection.rollback()
            return None
    
    def get_code_info(self, code: str) -> Optional[Dict[str, Any]]:
        """Get information about a marketing code."""
        try:
            self.cursor.execute('''
                SELECT id, code, description, discount_percent, max_uses, current_uses,
                       valid_from, valid_until, is_active, created_at
                FROM marketing_codes WHERE code = ?
            ''', (code,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'code': row[1],
                    'description': row[2],
                    'discount_percent': row[3],
                    'max_uses': row[4],
                    'current_uses': row[5],
                    'valid_from': row[6],
                    'valid_until': row[7],
                    'is_active': bool(row[8]),
                    'created_at': row[9]
                }
            return None
            
        except Exception as e:
            print(f"❌ Failed to get code info: {e}")
            return None
    
    def is_code_valid(self, code: str) -> Dict[str, Any]:
        """Check if a marketing code is valid for use."""
        code_info = self.get_code_info(code)
        if not code_info:
            return {'valid': False, 'reason': 'Code not found'}
        
        if not code_info['is_active']:
            return {'valid': False, 'reason': 'Code is inactive'}
        
        if code_info['valid_until'] and datetime.fromisoformat(code_info['valid_until']) < datetime.now():
            return {'valid': False, 'reason': 'Code has expired'}
        
        if code_info['max_uses'] > 0 and code_info['current_uses'] >= code_info['max_uses']:
            return {'valid': False, 'reason': 'Code usage limit reached'}
        
        return {'valid': True, 'code_info': code_info}
    
    def use_code(self, code: str, user_id: Optional[int] = None, 
                ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
        """Use a marketing code."""
        validation = self.is_code_valid(code)
        if not validation['valid']:
            return validation
        
        code_info = validation['code_info']
        
        try:
            # Update usage count
            self.cursor.execute('''
                UPDATE marketing_codes 
                SET current_uses = current_uses + 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (code_info['id'],))
            
            # Log usage
            self.cursor.execute('''
                INSERT INTO code_usage_log (code_id, user_id, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ''', (code_info['id'], user_id, ip_address, user_agent))
            
            self.connection.commit()
            
            return {
                'valid': True,
                'code': code,
                'discount_percent': code_info['discount_percent'],
                'description': code_info['description'],
                'message': 'Code used successfully'
            }
            
        except Exception as e:
            print(f"❌ Failed to use code: {e}")
            self.connection.rollback()
            return {'valid': False, 'reason': 'Database error'}
    
    def get_all_codes(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all marketing codes."""
        try:
            query = '''
                SELECT id, code, description, discount_percent, max_uses, current_uses,
                       valid_from, valid_until, is_active, created_at
                FROM marketing_codes
            '''
            
            if active_only:
                query += " WHERE is_active = 1"
            
            query += " ORDER BY created_at DESC"
            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            codes = []
            for row in rows:
                codes.append({
                    'id': row[0],
                    'code': row[1],
                    'description': row[2],
                    'discount_percent': row[3],
                    'max_uses': row[4],
                    'current_uses': row[5],
                    'valid_from': row[6],
                    'valid_until': row[7],
                    'is_active': bool(row[8]),
                    'created_at': row[9]
                })
            
            return codes
            
        except Exception as e:
            print(f"❌ Failed to get codes: {e}")
            return []
    
    def update_code(self, code: str, **kwargs) -> bool:
        """Update a marketing code."""
        try:
            allowed_fields = ['description', 'discount_percent', 'max_uses', 'valid_until', 'is_active']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = ?")
                    values.append(value)
            
            if not updates:
                return False
            
            values.append(code)
            query = f"UPDATE marketing_codes SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE code = ?"
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            print(f"✅ Updated marketing code: {code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update code: {e}")
            self.connection.rollback()
            return False
    
    def delete_code(self, code: str) -> bool:
        """Delete a marketing code."""
        try:
            self.cursor.execute("DELETE FROM marketing_codes WHERE code = ?", (code,))
            self.connection.commit()
            
            print(f"✅ Deleted marketing code: {code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete code: {e}")
            self.connection.rollback()
            return False
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get marketing code usage statistics."""
        try:
            # Total codes
            self.cursor.execute("SELECT COUNT(*) FROM marketing_codes")
            total_codes = self.cursor.fetchone()[0]
            
            # Active codes
            self.cursor.execute("SELECT COUNT(*) FROM marketing_codes WHERE is_active = 1")
            active_codes = self.cursor.fetchone()[0]
            
            # Total usage
            self.cursor.execute("SELECT SUM(current_uses) FROM marketing_codes")
            total_usage = self.cursor.fetchone()[0] or 0
            
            # Most used codes
            self.cursor.execute('''
                SELECT code, description, current_uses 
                FROM marketing_codes 
                ORDER BY current_uses DESC 
                LIMIT 5
            ''')
            top_codes = [{'code': row[0], 'description': row[1], 'uses': row[2]} for row in self.cursor.fetchall()]
            
            return {
                'total_codes': total_codes,
                'active_codes': active_codes,
                'total_usage': total_usage,
                'top_codes': top_codes
            }
            
        except Exception as e:
            print(f"❌ Failed to get statistics: {e}")
            return {}

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Marketing Code Manager for Yourl.Cloud')
    parser.add_argument('action', choices=['create', 'list', 'info', 'use', 'update', 'delete', 'stats'],
                       help='Action to perform')
    parser.add_argument('--code', '-c', help='Marketing code')
    parser.add_argument('--description', '-d', help='Code description')
    parser.add_argument('--discount', '-p', type=float, help='Discount percentage')
    parser.add_argument('--max-uses', '-m', type=int, help='Maximum uses')
    parser.add_argument('--valid-days', '-v', type=int, help='Valid days')
    parser.add_argument('--db-path', '-b', default='yourl_cloud.db', help='Database file path')
    
    args = parser.parse_args()
    
    manager = MarketingCodeManager(args.db_path)
    
    try:
        if not manager.connect():
            exit(1)
        
        manager.ensure_tables_exist()
        
        if args.action == 'create':
            if not args.description:
                print("❌ Description required for create action")
                exit(1)
            
            code = manager.create_code(
                description=args.description,
                discount_percent=args.discount or 0.0,
                max_uses=args.max_uses or -1,
                valid_days=args.valid_days or 30
            )
            
            if code:
                print(f"✅ Created code: {code}")
            else:
                exit(1)
                
        elif args.action == 'list':
            codes = manager.get_all_codes()
            print(f"📋 Found {len(codes)} marketing codes:")
            for code_info in codes:
                print(f"  {code_info['code']}: {code_info['description']} ({code_info['discount_percent']}% off)")
                
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
            if not args.code:
                print("❌ Code required for use action")
                exit(1)
            
            result = manager.use_code(args.code)
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
            if args.discount is not None:
                updates['discount_percent'] = args.discount
            if args.max_uses is not None:
                updates['max_uses'] = args.max_uses
            
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
