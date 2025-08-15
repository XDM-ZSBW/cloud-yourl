# Test Local Clipboard History - Standalone Offline Instance
# =========================================================
#
# This script provides a standalone test environment for Windows clipboard
# history integration that can be run from IDE terminals.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
# Environment: Local Test

import argparse
import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import hashlib
import re

class TestClipboardHistory:
    """
    Standalone test environment for clipboard history functionality.
    Uses local SQLite database for testing without external dependencies.
    """
    
    def __init__(self, db_path: str = "test_clipboard.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the test database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create clipboard history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clipboard_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                content_hash TEXT UNIQUE,
                tags TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                format TEXT DEFAULT 'text',
                size INTEGER,
                source TEXT DEFAULT 'test'
            )
        ''')
        
        # Create tags table for better organization
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create clipboard_tags junction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clipboard_tags (
                clipboard_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (clipboard_id) REFERENCES clipboard_history (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id),
                PRIMARY KEY (clipboard_id, tag_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_clipboard_item(self, content: str, tags: List[str] = None, format: str = "text") -> Dict:
        """Add a new clipboard item to the test database."""
        if not content:
            return {'status': 'error', 'message': 'Content cannot be empty'}
        
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert clipboard content
            cursor.execute('''
                INSERT OR REPLACE INTO clipboard_history 
                (content, content_hash, tags, format, size, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (content, content_hash, json.dumps(tags or []), format, len(content), 'test'))
            
            clipboard_id = cursor.lastrowid
            
            # Handle tags
            if tags:
                for tag_name in tags:
                    # Insert tag if it doesn't exist
                    cursor.execute('''
                        INSERT OR IGNORE INTO tags (name) VALUES (?)
                    ''', (tag_name,))
                    
                    tag_id = cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,)).fetchone()[0]
                    
                    # Link tag to clipboard item
                    cursor.execute('''
                        INSERT OR IGNORE INTO clipboard_tags (clipboard_id, tag_id)
                        VALUES (?, ?)
                    ''', (clipboard_id, tag_id))
            
            conn.commit()
            
            return {
                'status': 'success',
                'id': clipboard_id,
                'content_hash': content_hash,
                'message': 'Clipboard item added successfully'
            }
            
        except Exception as e:
            conn.rollback()
            return {'status': 'error', 'message': f'Database error: {str(e)}'}
        finally:
            conn.close()
    
    def get_recent_items(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        """Get recent clipboard items from the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, content, tags, timestamp, format, size, source
            FROM clipboard_history
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (cutoff_time.isoformat(), limit))
        
        items = []
        for row in cursor.fetchall():
            items.append({
                'id': row[0],
                'content': row[1],
                'tags': json.loads(row[2]) if row[2] else [],
                'timestamp': row[3],
                'format': row[4],
                'size': row[5],
                'source': row[6]
            })
        
        conn.close()
        return items
    
    def search_items(self, query: str, hours: int = 24) -> List[Dict]:
        """Search clipboard items by content or tags."""
        if not query:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search in content and tags
        cursor.execute('''
            SELECT DISTINCT ch.id, ch.content, ch.tags, ch.timestamp, ch.format, ch.size, ch.source
            FROM clipboard_history ch
            LEFT JOIN clipboard_tags ct ON ch.id = ct.clipboard_id
            LEFT JOIN tags t ON ct.tag_id = t.id
            WHERE (ch.timestamp >= ?) AND 
                  (ch.content LIKE ? OR t.name LIKE ? OR ch.tags LIKE ?)
            ORDER BY ch.timestamp DESC
        ''', (cutoff_time.isoformat(), f'%{query}%', f'%{query}%', f'%{query}%'))
        
        items = []
        for row in cursor.fetchall():
            items.append({
                'id': row[0],
                'content': row[1],
                'tags': json.loads(row[2]) if row[2] else [],
                'timestamp': row[3],
                'format': row[4],
                'size': row[5],
                'source': row[6]
            })
        
        conn.close()
        return items
    
    def get_items_by_tag(self, tag: str, hours: int = 24) -> List[Dict]:
        """Get clipboard items that have a specific tag."""
        if not tag:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ch.id, ch.content, ch.tags, ch.timestamp, ch.format, ch.size, ch.source
            FROM clipboard_history ch
            JOIN clipboard_tags ct ON ch.id = ct.clipboard_id
            JOIN tags t ON ct.tag_id = t.id
            WHERE (ch.timestamp >= ?) AND (t.name = ?)
            ORDER BY ch.timestamp DESC
        ''', (cutoff_time.isoformat(), tag))
        
        items = []
        for row in cursor.fetchall():
            items.append({
                'id': row[0],
                'content': row[1],
                'tags': json.loads(row[2]) if row[2] else [],
                'timestamp': row[3],
                'format': row[4],
                'size': row[5],
                'source': row[6]
            })
        
        conn.close()
        return items
    
    def get_statistics(self) -> Dict:
        """Get clipboard history statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total items
        cursor.execute('SELECT COUNT(*) FROM clipboard_history')
        total_items = cursor.fetchone()[0]
        
        # Items in last 24 hours
        yesterday = datetime.now() - timedelta(hours=24)
        cursor.execute('SELECT COUNT(*) FROM clipboard_history WHERE timestamp >= ?', (yesterday.isoformat(),))
        recent_items = cursor.fetchone()[0]
        
        # Total tags
        cursor.execute('SELECT COUNT(*) FROM tags')
        total_tags = cursor.fetchone()[0]
        
        # Most used tags
        cursor.execute('''
            SELECT t.name, COUNT(ct.clipboard_id) as usage_count
            FROM tags t
            JOIN clipboard_tags ct ON t.id = ct.tag_id
            GROUP BY t.id, t.name
            ORDER BY usage_count DESC
            LIMIT 5
        ''')
        top_tags = [{'tag': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Average content size
        cursor.execute('SELECT AVG(size) FROM clipboard_history WHERE size > 0')
        avg_size = cursor.fetchone()[0] or 0
        
        # Format distribution
        cursor.execute('''
            SELECT format, COUNT(*) as count
            FROM clipboard_history
            GROUP BY format
            ORDER BY count DESC
        ''')
        format_distribution = [{'format': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total_items': total_items,
            'recent_items_24h': recent_items,
            'total_tags': total_tags,
            'top_tags': top_tags,
            'average_content_size': round(avg_size, 2),
            'format_distribution': format_distribution,
            'database_path': self.db_path
        }
    
    def clear_all_data(self) -> Dict:
        """Clear all test data from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM clipboard_tags')
            cursor.execute('DELETE FROM clipboard_history')
            cursor.execute('DELETE FROM tags')
            conn.commit()
            
            return {'status': 'success', 'message': 'All test data cleared'}
            
        except Exception as e:
            conn.rollback()
            return {'status': 'error', 'message': f'Error clearing data: {str(e)}'}
        finally:
            conn.close()
    
    def generate_test_data(self, count: int = 10) -> Dict:
        """Generate sample test data for testing purposes."""
        test_contents = [
            "Hello from Yourl.Cloud!",
            "Test clipboard content 1",
            "Sample text for testing",
            "Yourl.Cloud marketing code: YC12345",
            "Clipboard bridge integration test",
            "Windows clipboard history test",
            "Zaido clipboard conflict test",
            "Test data with tags",
            "Sample content for search",
            "Another test entry"
        ]
        
        test_tags = ['test', 'yourl-cloud', 'clipboard', 'windows', 'zaido', 'sample']
        
        added_count = 0
        for i in range(min(count, len(test_contents))):
            content = test_contents[i]
            tags = [test_tags[i % len(test_tags)], test_tags[(i + 1) % len(test_tags)]
            
            result = self.add_clipboard_item(content, tags)
            if result['status'] == 'success':
                added_count += 1
        
        return {
            'status': 'success',
            'message': f'Generated {added_count} test items',
            'items_added': added_count
        }

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Test Local Clipboard History')
    parser.add_argument('action', choices=['display', 'search', 'recent', 'tags', 'stats', 'clear', 'add', 'generate'],
                       help='Action to perform')
    parser.add_argument('--query', '-q', help='Search query for search action')
    parser.add_argument('--tags', '-t', nargs='*', help='Tags for add action or filter')
    parser.add_argument('--hours', '-h', type=int, default=24, help='Hours to look back')
    parser.add_argument('--content', '-c', help='Content for add action')
    parser.add_argument('--count', '-n', type=int, default=10, help='Number of test items to generate')
    
    args = parser.parse_args()
    
    clipboard = TestClipboardHistory()
    
    if args.action == 'display':
        items = clipboard.get_recent_items(args.hours)
        print(f"📋 Recent clipboard items (last {args.hours}h):")
        for item in items:
            print(f"  [{item['timestamp']}] {item['content'][:80]}...")
            if item['tags']:
                print(f"    Tags: {', '.join(item['tags'])}")
    
    elif args.action == 'search':
        if not args.query:
            print("❌ Search query required for search action")
            return
        results = clipboard.search_items(args.query, args.hours)
        print(f"🔍 Found {len(results)} results for '{args.query}':")
        for item in results:
            print(f"  [{item['timestamp']}] {item['content'][:80]}...")
    
    elif args.action == 'recent':
        items = clipboard.get_recent_items(args.hours)
        print(f"📋 Recent items (last {args.hours}h): {len(items)} items")
        for item in items[:5]:  # Show first 5
            print(f"  [{item['timestamp']}] {item['content'][:60]}...")
    
    elif args.action == 'tags':
        if args.tags:
            for tag in args.tags:
                items = clipboard.get_items_by_tag(tag, args.hours)
                print(f"🏷️ Items with tag '{tag}' (last {args.hours}h): {len(items)} items")
                for item in items[:3]:  # Show first 3
                    print(f"  [{item['timestamp']}] {item['content'][:60]}...")
        else:
            print("❌ Tags required for tags action")
    
    elif args.action == 'stats':
        stats = clipboard.get_statistics()
        print("📊 Clipboard History Statistics:")
        print(json.dumps(stats, indent=2))
    
    elif args.action == 'clear':
        result = clipboard.clear_all_data()
        print(json.dumps(result, indent=2))
    
    elif args.action == 'add':
        if not args.content:
            print("❌ Content required for add action")
            return
        result = clipboard.add_clipboard_item(args.content, args.tags or [])
        print(json.dumps(result, indent=2))
    
    elif args.action == 'generate':
        result = clipboard.generate_test_data(args.count)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
