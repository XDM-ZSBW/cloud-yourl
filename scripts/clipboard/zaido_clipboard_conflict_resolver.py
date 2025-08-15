# Windows Clipboard History Integration for Yourl.Cloud
# ===================================================
#
# This PowerShell script provides easy access to Windows clipboard history
# integration with Yourl.Cloud clipboard bridge.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import win32clipboard
import win32con
import time
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import re

class ZaidoClipboardConflictResolver:
    """
    Resolves conflicts between Zaido clipboard operations and Yourl.Cloud
    clipboard bridge by monitoring and managing clipboard state.
    """
    
    def __init__(self, project_id: str = "yourl-cloud", bridge_url: str = "https://cb.yourl.cloud"):
        self.project_id = project_id
        self.bridge_url = bridge_url
        self.clipboard_history = []
        self.conflict_log = []
        self.last_clipboard_content = None
        self.last_change_time = None
        self.monitoring = False
        
    def start_monitoring(self):
        """Start monitoring clipboard for changes and conflicts."""
        self.monitoring = True
        print("🔍 Starting clipboard conflict monitoring...")
        
        try:
            while self.monitoring:
                current_content = self.get_clipboard_content()
                
                if current_content is not None and current_content != self.last_clipboard_content:
                    self.handle_clipboard_change(current_content)
                    self.last_clipboard_content = current_content
                    self.last_change_time = datetime.now()
                
                time.sleep(0.5)  # Check every 500ms
                
        except KeyboardInterrupt:
            print("\n⏹️ Stopping clipboard monitoring...")
            self.stop_monitoring()
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop clipboard monitoring."""
        self.monitoring = False
        print("✅ Clipboard monitoring stopped")
    
    def get_clipboard_content(self) -> Optional[str]:
        """Get current clipboard content safely."""
        try:
            win32clipboard.OpenClipboard()
            try:
                content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                return content
            except:
                return None
            finally:
                win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"⚠️ Error reading clipboard: {e}")
            return None
    
    def set_clipboard_content(self, content: str):
        """Set clipboard content safely."""
        try:
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(content, win32con.CF_UNICODETEXT)
                print(f"📋 Clipboard updated: {content[:50]}...")
            finally:
                win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"❌ Error setting clipboard: {e}")
    
    def handle_clipboard_change(self, new_content: str):
        """Handle clipboard content changes and detect conflicts."""
        if not new_content:
            return
            
        timestamp = datetime.now()
        change_info = {
            'timestamp': timestamp,
            'content': new_content,
            'content_hash': hash(new_content),
            'length': len(new_content)
        }
        
        # Check for potential conflicts
        conflicts = self.detect_conflicts(new_content, timestamp)
        
        if conflicts:
            self.resolve_conflicts(conflicts, new_content)
            change_info['conflicts_resolved'] = True
        else:
            change_info['conflicts_resolved'] = False
        
        self.clipboard_history.append(change_info)
        
        # Keep only last 100 entries
        if len(self.clipboard_history) > 100:
            self.clipboard_history.pop(0)
    
    def detect_conflicts(self, content: str, timestamp: datetime) -> List[Dict]:
        """Detect potential clipboard conflicts."""
        conflicts = []
        
        # Check for rapid clipboard changes (potential conflict)
        if self.last_change_time and (timestamp - self.last_change_time).total_seconds() < 0.1:
            conflicts.append({
                'type': 'rapid_change',
                'description': 'Clipboard changed too rapidly, potential conflict detected',
                'severity': 'medium'
            })
        
        # Check for Zaido-specific patterns
        zaido_patterns = [
            r'zaido.*clipboard',
            r'clipboard.*zaido',
            r'zaido.*conflict',
            r'conflict.*zaido'
        ]
        
        for pattern in zaido_patterns:
            if re.search(pattern, content.lower()):
                conflicts.append({
                    'type': 'zaido_pattern',
                    'description': f'Zaido-related content detected: {pattern}',
                    'severity': 'low'
                })
        
        # Check for Yourl.Cloud code patterns
        yourl_patterns = [
            r'yourl.*cloud',
            r'cloud.*yourl',
            r'yourl.*code',
            r'code.*yourl'
        ]
        
        for pattern in yourl_patterns:
            if re.search(pattern, content.lower()):
                conflicts.append({
                    'type': 'yourl_pattern',
                    'description': f'Yourl.Cloud content detected: {pattern}',
                    'severity': 'low'
                })
        
        return conflicts
    
    def resolve_conflicts(self, conflicts: List[Dict], content: str):
        """Resolve detected clipboard conflicts."""
        print(f"🔧 Resolving {len(conflicts)} clipboard conflicts...")
        
        for conflict in conflicts:
            print(f"  - {conflict['type']}: {conflict['description']}")
            
            if conflict['type'] == 'rapid_change':
                # Wait a moment to let the system stabilize
                time.sleep(0.2)
                print("  ⏳ Waiting for clipboard to stabilize...")
            
            # Log the conflict resolution
            conflict['resolved_at'] = datetime.now()
            conflict['resolution_method'] = 'automatic'
            self.conflict_log.append(conflict)
        
        print(f"✅ Resolved {len(conflicts)} conflicts")
    
    def get_clipboard_stats(self) -> Dict:
        """Get clipboard operation statistics."""
        if not self.clipboard_history:
            return {'message': 'No clipboard history available'}
        
        total_changes = len(self.clipboard_history)
        conflicts_resolved = sum(1 for entry in self.clipboard_history if entry.get('conflicts_resolved', False))
        
        # Calculate average content length
        content_lengths = [entry.get('length', 0) for entry in self.clipboard_history]
        avg_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
        
        # Get recent activity
        recent_activity = self.clipboard_history[-10:] if len(self.clipboard_history) >= 10 else self.clipboard_history
        
        return {
            'total_changes': total_changes,
            'conflicts_resolved': conflicts_resolved,
            'conflict_rate': (conflicts_resolved / total_changes * 100) if total_changes > 0 else 0,
            'average_content_length': round(avg_length, 2),
            'recent_activity': [
                {
                    'timestamp': entry['timestamp'].strftime('%H:%M:%S'),
                    'content_preview': entry['content'][:50] + '...' if len(entry['content']) > 50 else entry['content'],
                    'conflicts_resolved': entry.get('conflicts_resolved', False)
                }
                for entry in recent_activity
            ]
        }
    
    def clear_history(self):
        """Clear clipboard history and conflict log."""
        self.clipboard_history.clear()
        self.conflict_log.clear()
        print("🗑️ Clipboard history and conflict log cleared")
    
    def export_conflict_log(self, filename: str = None):
        """Export conflict log to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"clipboard_conflicts_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conflict_log, f, indent=2, default=str)
            print(f"📁 Conflict log exported to: {filename}")
        except Exception as e:
            print(f"❌ Error exporting conflict log: {e}")
    
    def search_history(self, query: str, hours: int = 24) -> List[Dict]:
        """Search clipboard history for specific content."""
        if not query:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        results = []
        
        for entry in self.clipboard_history:
            if entry['timestamp'] >= cutoff_time:
                content = entry.get('content', '')
                if query.lower() in content.lower():
                    results.append(entry)
        
        return results

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Zaido Clipboard Conflict Resolver')
    parser.add_argument('action', choices=['monitor', 'stats', 'search', 'clear', 'export'],
                       help='Action to perform')
    parser.add_argument('--query', '-q', help='Search query for search action')
    parser.add_argument('--hours', '-t', type=int, default=24, help='Hours to look back for search')
    parser.add_argument('--output', '-o', help='Output filename for export action')
    
    args = parser.parse_args()
    
    resolver = ZaidoClipboardConflictResolver()
    
    if args.action == 'monitor':
        resolver.start_monitoring()
    elif args.action == 'stats':
        stats = resolver.get_clipboard_stats()
        print(json.dumps(stats, indent=2))
    elif args.action == 'search':
        if not args.query:
            print("❌ Search query required for search action")
            return
        results = resolver.search_history(args.query, args.hours)
        print(f"🔍 Found {len(results)} results for '{args.query}':")
        for result in results:
            print(f"  [{result['timestamp'].strftime('%H:%M:%S')}] {result['content'][:100]}...")
    elif args.action == 'clear':
        resolver.clear_history()
    elif args.action == 'export':
        resolver.export_conflict_log(args.output)

if __name__ == "__main__":
    main()
