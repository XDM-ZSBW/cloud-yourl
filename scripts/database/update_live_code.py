# Update Live Code for Yourl.Cloud
# =================================
#
# This script updates live marketing codes and manages code rotation
# for Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import json
import secrets
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

class LiveCodeUpdater:
    """Live code update and rotation management class."""
    
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
        """Ensure required tables exist."""
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
            
            # Live codes table for active codes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS live_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_id INTEGER NOT NULL,
                    is_live BOOLEAN DEFAULT 1,
                    activated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    deactivated_at DATETIME,
                    rotation_order INTEGER DEFAULT 0,
                    FOREIGN KEY (code_id) REFERENCES marketing_codes (id)
                )
            ''')
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def get_live_codes(self) -> List[Dict[str, Any]]:
        """Get currently live marketing codes."""
        try:
            self.cursor.execute('''
                SELECT mc.id, mc.code, mc.description, mc.discount_percent,
                       mc.max_uses, mc.current_uses, mc.valid_until,
                       lc.activated_at, lc.rotation_order
                FROM marketing_codes mc
                JOIN live_codes lc ON mc.id = lc.code_id
                WHERE lc.is_live = 1 AND mc.is_active = 1
                ORDER BY lc.rotation_order ASC
            ''')
            
            rows = self.cursor.fetchall()
            live_codes = []
            
            for row in rows:
                live_codes.append({
                    'id': row[0],
                    'code': row[1],
                    'description': row[2],
                    'discount_percent': row[3],
                    'max_uses': row[4],
                    'current_uses': row[5],
                    'valid_until': row[6],
                    'activated_at': row[7],
                    'rotation_order': row[8]
                })
            
            return live_codes
            
        except Exception as e:
            print(f"❌ Failed to get live codes: {e}")
            return []
    
    def activate_code(self, code: str) -> bool:
        """Activate a marketing code as live."""
        try:
            # Get code ID
            self.cursor.execute("SELECT id FROM marketing_codes WHERE code = ?", (code,))
            row = self.cursor.fetchone()
            if not row:
                print(f"❌ Code not found: {code}")
                return False
            
            code_id = row[0]
            
            # Check if already live
            self.cursor.execute("SELECT id FROM live_codes WHERE code_id = ? AND is_live = 1", (code_id,))
            if self.cursor.fetchone():
                print(f"⚠️ Code already live: {code}")
                return True
            
            # Get next rotation order
            self.cursor.execute("SELECT MAX(rotation_order) FROM live_codes")
            max_order = self.cursor.fetchone()[0] or 0
            next_order = max_order + 1
            
            # Activate code
            self.cursor.execute('''
                INSERT INTO live_codes (code_id, is_live, activated_at, rotation_order)
                VALUES (?, 1, CURRENT_TIMESTAMP, ?)
            ''', (code_id, next_order))
            
            self.connection.commit()
            print(f"✅ Activated code: {code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to activate code: {e}")
            self.connection.rollback()
            return False
    
    def deactivate_code(self, code: str) -> bool:
        """Deactivate a live marketing code."""
        try:
            # Get code ID
            self.cursor.execute("SELECT id FROM marketing_codes WHERE code = ?", (code,))
            row = self.cursor.fetchone()
            if not row:
                print(f"❌ Code not found: {code}")
                return False
            
            code_id = row[0]
            
            # Deactivate code
            self.cursor.execute('''
                UPDATE live_codes 
                SET is_live = 0, deactivated_at = CURRENT_TIMESTAMP
                WHERE code_id = ? AND is_live = 1
            ''', (code_id,))
            
            if self.cursor.rowcount == 0:
                print(f"⚠️ Code not live: {code}")
                return True
            
            self.connection.commit()
            print(f"✅ Deactivated code: {code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to deactivate code: {e}")
            self.connection.rollback()
            return False
    
    def rotate_codes(self, keep_count: int = 3) -> bool:
        """Rotate live codes, keeping only the specified number active."""
        try:
            print(f"🔄 Rotating codes, keeping {keep_count} active...")
            
            # Get current live codes ordered by rotation
            live_codes = self.get_live_codes()
            
            if len(live_codes) <= keep_count:
                print(f"ℹ️ Only {len(live_codes)} codes active, no rotation needed")
                return True
            
            # Deactivate codes beyond the keep count
            codes_to_deactivate = live_codes[keep_count:]
            
            for code_info in codes_to_deactivate:
                self.deactivate_code(code_info['code'])
            
            print(f"✅ Rotated codes: {len(codes_to_deactivate)} deactivated")
            return True
            
        except Exception as e:
            print(f"❌ Code rotation failed: {e}")
            return False
    
    def update_code_rotation(self, code: str, new_order: int) -> bool:
        """Update the rotation order of a live code."""
        try:
            # Get code ID
            self.cursor.execute("SELECT id FROM marketing_codes WHERE code = ?", (code,))
            row = self.cursor.fetchone()
            if not row:
                print(f"❌ Code not found: {code}")
                return False
            
            code_id = row[0]
            
            # Update rotation order
            self.cursor.execute('''
                UPDATE live_codes 
                SET rotation_order = ?
                WHERE code_id = ? AND is_live = 1
            ''', (new_order, code_id))
            
            if self.cursor.rowcount == 0:
                print(f"⚠️ Code not live: {code}")
                return False
            
            self.connection.commit()
            print(f"✅ Updated rotation order for {code}: {new_order}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update rotation order: {e}")
            self.connection.rollback()
            return False
    
    def get_rotation_status(self) -> Dict[str, Any]:
        """Get current code rotation status."""
        try:
            live_codes = self.get_live_codes()
            
            # Get deactivated codes
            self.cursor.execute('''
                SELECT mc.code, mc.description, lc.deactivated_at, lc.rotation_order
                FROM marketing_codes mc
                JOIN live_codes lc ON mc.id = lc.code_id
                WHERE lc.is_live = 0
                ORDER BY lc.deactivated_at DESC
            ''')
            
            deactivated_codes = []
            for row in self.cursor.fetchall():
                deactivated_codes.append({
                    'code': row[0],
                    'description': row[1],
                    'deactivated_at': row[2],
                    'rotation_order': row[3]
                })
            
            return {
                'live_codes': live_codes,
                'deactivated_codes': deactivated_codes,
                'total_live': len(live_codes),
                'total_deactivated': len(deactivated_codes)
            }
            
        except Exception as e:
            print(f"❌ Failed to get rotation status: {e}")
            return {}
    
    def cleanup_expired_codes(self) -> bool:
        """Clean up expired marketing codes from live rotation."""
        try:
            print("🧹 Cleaning up expired codes...")
            
            # Get expired live codes
            self.cursor.execute('''
                SELECT mc.code, mc.valid_until
                FROM marketing_codes mc
                JOIN live_codes lc ON mc.id = lc.code_id
                WHERE lc.is_live = 1 
                AND mc.valid_until IS NOT NULL 
                AND mc.valid_until < CURRENT_TIMESTAMP
            ''')
            
            expired_codes = self.cursor.fetchall()
            
            if not expired_codes:
                print("ℹ️ No expired codes found")
                return True
            
            # Deactivate expired codes
            for code, valid_until in expired_codes:
                print(f"  Deactivating expired code: {code} (expired: {valid_until})")
                self.deactivate_code(code)
            
            print(f"✅ Cleaned up {len(expired_codes)} expired codes")
            return True
            
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            return False

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Live Code Updater for Yourl.Cloud')
    parser.add_argument('action', choices=['list', 'activate', 'deactivate', 'rotate', 'status', 'cleanup'],
                       help='Action to perform')
    parser.add_argument('--code', '-c', help='Marketing code')
    parser.add_argument('--keep-count', '-k', type=int, default=3, help='Number of codes to keep active')
    parser.add_argument('--order', '-o', type=int, help='New rotation order')
    parser.add_argument('--db-path', '-d', default='yourl_cloud.db', help='Database file path')
    
    args = parser.parse_args()
    
    updater = LiveCodeUpdater(args.db_path)
    
    try:
        if not updater.connect():
            exit(1)
        
        updater.ensure_tables_exist()
        
        if args.action == 'list':
            live_codes = updater.get_live_codes()
            print(f"📋 Found {len(live_codes)} live codes:")
            for code_info in live_codes:
                print(f"  [{code_info['rotation_order']}] {code_info['code']}: {code_info['description']}")
                
        elif args.action == 'activate':
            if not args.code:
                print("❌ Code required for activate action")
                exit(1)
            
            success = updater.activate_code(args.code)
            exit(0 if success else 1)
            
        elif args.action == 'deactivate':
            if not args.code:
                print("❌ Code required for deactivate action")
                exit(1)
            
            success = updater.deactivate_code(args.code)
            exit(0 if success else 1)
            
        elif args.action == 'rotate':
            success = updater.rotate_codes(args.keep_count)
            exit(0 if success else 1)
            
        elif args.action == 'status':
            status = updater.get_rotation_status()
            print(json.dumps(status, indent=2, default=str))
            
        elif args.action == 'cleanup':
            success = updater.cleanup_expired_codes()
            exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
    finally:
        updater.disconnect()

if __name__ == "__main__":
    main()
