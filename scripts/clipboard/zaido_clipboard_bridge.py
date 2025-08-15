# Zaido Clipboard Bridge for Yourl.Cloud
# =====================================
#
# This script provides a bridge between Zaido clipboard operations
# and Yourl.Cloud clipboard bridge service.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import requests
import json
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import hashlib
import base64

class ZaidoClipboardBridge:
    """
    Bridge between Zaido clipboard operations and Yourl.Cloud clipboard bridge.
    Handles synchronization, conflict resolution, and data transformation.
    """
    
    def __init__(self, bridge_url: str = "https://cb.yourl.cloud", project_id: str = "yourl-cloud"):
        self.bridge_url = bridge_url
        self.project_id = project_id
        self.session = requests.Session()
        self.last_sync_time = None
        self.sync_interval = 30  # seconds
        self.clipboard_cache = {}
        self.conflict_resolution_enabled = True
        
        # Configure session headers
        self.session.headers.update({
            'User-Agent': 'ZaidoClipboardBridge/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def sync_clipboard_data(self, clipboard_data: Dict) -> Dict:
        """Sync clipboard data with Yourl.Cloud bridge."""
        try:
            # Check if sync is needed
            if not self._should_sync():
                return {'status': 'skipped', 'reason': 'sync_not_due'}
            
            # Prepare data for sync
            sync_payload = self._prepare_sync_payload(clipboard_data)
            
            # Send to bridge
            response = self.session.post(
                f"{self.bridge_url}/api/sync",
                json=sync_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.last_sync_time = datetime.now()
                self._update_cache(clipboard_data, result)
                return {'status': 'success', 'data': result}
            else:
                return {'status': 'error', 'code': response.status_code, 'message': response.text}
                
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': f'Network error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    def _should_sync(self) -> bool:
        """Check if sync is needed based on time interval."""
        if self.last_sync_time is None:
            return True
        
        time_since_last_sync = datetime.now() - self.last_sync_time
        return time_since_last_sync.total_seconds() >= self.sync_interval
    
    def _prepare_sync_payload(self, clipboard_data: Dict) -> Dict:
        """Prepare clipboard data for sync with bridge."""
        # Generate content hash for change detection
        content_hash = hashlib.sha256(
            clipboard_data.get('content', '').encode('utf-8')
        ).hexdigest()
        
        payload = {
            'project_id': self.project_id,
            'timestamp': datetime.now().isoformat(),
            'content': clipboard_data.get('content', ''),
            'content_hash': content_hash,
            'metadata': {
                'source': 'zaido',
                'version': '1.0',
                'tags': clipboard_data.get('tags', []),
                'format': clipboard_data.get('format', 'text'),
                'size': len(clipboard_data.get('content', ''))
            }
        }
        
        # Add conflict resolution data if enabled
        if self.conflict_resolution_enabled:
            payload['conflict_resolution'] = {
                'enabled': True,
                'strategy': 'timestamp_based',
                'priority': 'zaido_first'
            }
        
        return payload
    
    def _update_cache(self, clipboard_data: Dict, sync_result: Dict):
        """Update local cache with sync results."""
        content_hash = clipboard_data.get('content_hash', '')
        if content_hash:
            self.clipboard_cache[content_hash] = {
                'data': clipboard_data,
                'sync_result': sync_result,
                'last_updated': datetime.now()
            }
    
    def resolve_conflicts(self, local_data: Dict, remote_data: Dict) -> Dict:
        """Resolve conflicts between local and remote clipboard data."""
        if not self.conflict_resolution_enabled:
            return local_data
        
        # Simple timestamp-based conflict resolution
        local_timestamp = datetime.fromisoformat(local_data.get('timestamp', '1970-01-01T00:00:00'))
        remote_timestamp = datetime.fromisoformat(remote_data.get('timestamp', '1970-01-01T00:00:00'))
        
        if local_timestamp > remote_timestamp:
            return local_data
        else:
            return remote_data
    
    def get_sync_status(self) -> Dict:
        """Get current sync status and statistics."""
        return {
            'last_sync': self.last_sync_time.isoformat() if self.last_sync_time else None,
            'sync_interval': self.sync_interval,
            'cache_size': len(self.clipboard_cache),
            'conflict_resolution': self.conflict_resolution_enabled,
            'bridge_url': self.bridge_url,
            'project_id': self.project_id
        }
    
    def set_sync_interval(self, seconds: int):
        """Set sync interval in seconds."""
        if seconds > 0:
            self.sync_interval = seconds
            return {'status': 'success', 'new_interval': seconds}
        else:
            return {'status': 'error', 'message': 'Interval must be positive'}
    
    def enable_conflict_resolution(self, enabled: bool = True):
        """Enable or disable conflict resolution."""
        self.conflict_resolution_enabled = enabled
        return {'status': 'success', 'conflict_resolution': enabled}
    
    def clear_cache(self):
        """Clear local clipboard cache."""
        self.clipboard_cache.clear()
        return {'status': 'success', 'message': 'Cache cleared'}
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        if not self.clipboard_cache:
            return {'message': 'Cache is empty'}
        
        total_size = sum(len(str(v)) for v in self.clipboard_cache.values())
        oldest_entry = min(self.clipboard_cache.values(), key=lambda x: x['last_updated'])
        newest_entry = max(self.clipboard_cache.values(), key=lambda x: x['last_updated'])
        
        return {
            'total_entries': len(self.clipboard_cache),
            'total_size_bytes': total_size,
            'oldest_entry': oldest_entry['last_updated'].isoformat(),
            'newest_entry': newest_entry['last_updated'].isoformat(),
            'average_entry_size': total_size / len(self.clipboard_cache) if self.clipboard_cache else 0
        }

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Zaido Clipboard Bridge')
    parser.add_argument('action', choices=['sync', 'status', 'config', 'clear-cache', 'stats'],
                       help='Action to perform')
    parser.add_argument('--content', '-c', help='Clipboard content to sync')
    parser.add_argument('--tags', '-t', nargs='*', help='Tags for the content')
    parser.add_argument('--format', '-f', default='text', help='Content format')
    parser.add_argument('--interval', '-i', type=int, help='Sync interval in seconds')
    parser.add_argument('--bridge-url', '-u', help='Bridge URL')
    parser.add_argument('--project-id', '-p', help='Project ID')
    
    args = parser.parse_args()
    
    # Initialize bridge
    bridge = ZaidoClipboardBridge(
        bridge_url=args.bridge_url or "https://cb.yourl.cloud",
        project_id=args.project_id or "yourl-cloud"
    )
    
    if args.action == 'sync':
        if not args.content:
            print("❌ Content required for sync action")
            return
        
        clipboard_data = {
            'content': args.content,
            'tags': args.tags or [],
            'format': args.format,
            'timestamp': datetime.now().isoformat()
        }
        
        result = bridge.sync_clipboard_data(clipboard_data)
        print(json.dumps(result, indent=2))
        
    elif args.action == 'status':
        status = bridge.get_sync_status()
        print(json.dumps(status, indent=2))
        
    elif args.action == 'config':
        if args.interval:
            result = bridge.set_sync_interval(args.interval)
            print(json.dumps(result, indent=2))
        else:
            print("❌ Configuration option required (e.g., --interval)")
            
    elif args.action == 'clear-cache':
        result = bridge.clear_cache()
        print(json.dumps(result, indent=2))
        
    elif args.action == 'stats':
        stats = bridge.get_cache_stats()
        print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()
