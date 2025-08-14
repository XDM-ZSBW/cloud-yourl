#!/usr/bin/env python3
"""
Windows Clipboard History Integration for Yourl.Cloud
====================================================

This script integrates Windows clipboard history with the Yourl.Cloud clipboard bridge
to help you find recent clipboard items from all your devices that contain your codes.

Features:
- Monitors Windows clipboard history
- Syncs with Yourl.Cloud clipboard bridge
- Searches for Yourl.Cloud codes across devices
- Provides quick access to recent clipboard items
- Integrates with Windows clipboard history (Win+V)

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
"""

import os
import sys
import json
import time
import hashlib
import requests
import threading
import subprocess
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('windows_clipboard_history')

@dataclass
class ClipboardHistoryItem:
    """Represents a Windows clipboard history item"""
    id: str
    content: str
    content_type: str  # 'text', 'image', 'file'
    source_device: str
    created_at: datetime
    accessed_at: datetime
    tags: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/transmission"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['accessed_at'] = self.accessed_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClipboardHistoryItem':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['accessed_at'] = datetime.fromisoformat(data['accessed_at'])
        return cls(**data)

class WindowsClipboardHistory:
    """Windows clipboard history integration with Yourl.Cloud"""
    
    def __init__(self, project_id: str = 'yourl-cloud', clipboard_bridge_url: str = 'https://cb.yourl.cloud'):
        self.project_id = project_id
        self.clipboard_bridge_url = clipboard_bridge_url
        self.history_items: Dict[str, ClipboardHistoryItem] = {}
        self.yourl_code_pattern = re.compile(r'\b[A-Z]{4,8}\d{2,3}[!@#$%^&*+=?~]\b')
        self.device_id = self._get_device_id()
        
        # Load existing history
        self._load_history()
        
        # Start monitoring thread
        self.monitoring = False
        self.monitor_thread = None
    
    def _get_device_id(self) -> str:
        """Get unique device identifier"""
        try:
            # Use hostname and user as device identifier
            hostname = os.environ.get('COMPUTERNAME', 'unknown')
            username = os.environ.get('USERNAME', 'unknown')
            return f"{hostname}-{username}"
        except Exception as e:
            logger.error(f"Failed to get device ID: {e}")
            return "unknown-device"
    
    def _load_history(self):
        """Load clipboard history from local storage"""
        try:
            history_file = os.path.expanduser("~/.yourl_clipboard_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    for item_data in data.get('items', []):
                        item = ClipboardHistoryItem.from_dict(item_data)
                        self.history_items[item.id] = item
                logger.info(f"Loaded {len(self.history_items)} clipboard history items")
        except Exception as e:
            logger.error(f"Failed to load clipboard history: {e}")
    
    def _save_history(self):
        """Save clipboard history to local storage"""
        try:
            history_file = os.path.expanduser("~/.yourl_clipboard_history.json")
            data = {
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'device_id': self.device_id,
                'items': [item.to_dict() for item in self.history_items.values()]
            }
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save clipboard history: {e}")
    
    def _generate_item_id(self, content: str) -> str:
        """Generate unique ID for clipboard item"""
        unique_string = f"{content[:50]}{self.device_id}{time.time()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def add_clipboard_item(self, content: str, content_type: str = 'text') -> Optional[ClipboardHistoryItem]:
        """Add a new clipboard item to history"""
        try:
            # Generate unique ID
            item_id = self._generate_item_id(content)
            
            # Check if item already exists (avoid duplicates)
            for existing_item in self.history_items.values():
                if existing_item.content == content:
                    # Update access time
                    existing_item.accessed_at = datetime.now(timezone.utc)
                    self._save_history()
                    return existing_item
            
            # Create new item
            item = ClipboardHistoryItem(
                id=item_id,
                content=content,
                content_type=content_type,
                source_device=self.device_id,
                created_at=datetime.now(timezone.utc),
                accessed_at=datetime.now(timezone.utc),
                tags=self._extract_tags(content),
                metadata=self._extract_metadata(content)
            )
            
            # Add to history
            self.history_items[item_id] = item
            
            # Save to local storage
            self._save_history()
            
            # Sync with clipboard bridge if it contains Yourl.Cloud codes
            if self._contains_yourl_codes(content):
                self._sync_with_clipboard_bridge(item)
            
            logger.info(f"Added clipboard item: {item_id[:8]}...")
            return item
            
        except Exception as e:
            logger.error(f"Failed to add clipboard item: {e}")
            return None
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from clipboard content"""
        tags = []
        
        # Check for Yourl.Cloud codes
        if self._contains_yourl_codes(content):
            tags.append('yourl-cloud-code')
        
        # Check for URLs
        if 'http' in content.lower():
            tags.append('url')
        
        # Check for email addresses
        if '@' in content and '.' in content:
            tags.append('email')
        
        # Check for phone numbers
        if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', content):
            tags.append('phone')
        
        return tags
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from clipboard content"""
        metadata = {
            'length': len(content),
            'has_yourl_codes': self._contains_yourl_codes(content),
            'content_preview': content[:100] + '...' if len(content) > 100 else content
        }
        
        # Extract Yourl.Cloud codes if present
        if self._contains_yourl_codes(content):
            codes = self.yourl_code_pattern.findall(content)
            metadata['yourl_codes'] = codes
        
        return metadata
    
    def _contains_yourl_codes(self, content: str) -> bool:
        """Check if content contains Yourl.Cloud codes"""
        return bool(self.yourl_code_pattern.search(content))
    
    def _sync_with_clipboard_bridge(self, item: ClipboardHistoryItem):
        """Sync item with Yourl.Cloud clipboard bridge"""
        try:
            if not self._contains_yourl_codes(item.content):
                return
            
            # Prepare data for clipboard bridge
            bridge_data = {
                "content": item.content,
                "content_type": "text",
                "source_location": self.device_id,
                "target_locations": ["all-devices"],
                "created_by": f"windows-clipboard-{self.device_id}",
                "priority": "medium",
                "tags": item.tags,
                "expires_in_hours": 168,  # 1 week
                "metadata": {
                    **item.metadata,
                    "source": "windows-clipboard-history",
                    "device_id": self.device_id
                }
            }
            
            # Send to clipboard bridge
            response = requests.post(
                f"{self.clipboard_bridge_url}/api/clipboard",
                json=bridge_data,
                timeout=10
            )
            
            if response.status_code == 201:
                logger.info(f"Synced clipboard item with bridge: {item.id[:8]}...")
            else:
                logger.warning(f"Failed to sync with bridge: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to sync with clipboard bridge: {e}")
    
    def search_clipboard_history(self, query: Optional[str] = None, tags: Optional[List[str]] = None, 
                                include_yourl_codes: bool = True) -> List[ClipboardHistoryItem]:
        """Search clipboard history for items"""
        results = []
        
        for item in self.history_items.values():
            # Check if item matches search criteria
            matches = True
            
            # Text search
            if query and query.lower() not in item.content.lower():
                matches = False
            
            # Tag search
            if tags and not any(tag in item.tags for tag in tags):
                matches = False
            
            # Yourl.Cloud codes filter
            if include_yourl_codes and not self._contains_yourl_codes(item.content):
                matches = False
            
            if matches:
                results.append(item)
        
        # Sort by access time (most recent first)
        results.sort(key=lambda x: x.accessed_at, reverse=True)
        
        return results
    
    def get_yourl_codes_from_history(self) -> List[ClipboardHistoryItem]:
        """Get all clipboard items containing Yourl.Cloud codes"""
        return self.search_clipboard_history(include_yourl_codes=True)
    
    def get_recent_items(self, hours: int = 24) -> List[ClipboardHistoryItem]:
        """Get recent clipboard items"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        recent_items = []
        
        for item in self.history_items.values():
            if item.accessed_at >= cutoff_time:
                recent_items.append(item)
        
        # Sort by access time (most recent first)
        recent_items.sort(key=lambda x: x.accessed_at, reverse=True)
        
        return recent_items
    
    def start_monitoring(self):
        """Start monitoring clipboard for new items"""
        if self.monitoring:
            logger.warning("Clipboard monitoring already started")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
        self.monitor_thread.start()
        logger.info("Started clipboard monitoring")
    
    def stop_monitoring(self):
        """Stop monitoring clipboard"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Stopped clipboard monitoring")
    
    def _monitor_clipboard(self):
        """Monitor clipboard for new items"""
        import win32clipboard
        import win32con
        
        last_content = None
        
        while self.monitoring:
            try:
                # Get current clipboard content
                win32clipboard.OpenClipboard()
                try:
                    if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                        content = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                        if isinstance(content, bytes):
                            content = content.decode('utf-8', errors='ignore')
                        
                        # Check if content changed
                        if content != last_content and content.strip():
                            self.add_clipboard_item(content)
                            last_content = content
                finally:
                    win32clipboard.CloseClipboard()
                
                # Wait before checking again
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error monitoring clipboard: {e}")
                time.sleep(5)
    
    def display_history(self, items: Optional[List[ClipboardHistoryItem]] = None, 
                       show_yourl_codes_only: bool = False):
        """Display clipboard history in a formatted way"""
        if items is None:
            if show_yourl_codes_only:
                items = self.get_yourl_codes_from_history()
            else:
                items = self.get_recent_items()
        
        if not items:
            print("No clipboard items found.")
            return
        
        print(f"\n📋 Clipboard History ({len(items)} items)")
        print("=" * 80)
        
        for i, item in enumerate(items, 1):
            print(f"\n{i}. {item.content[:50]}{'...' if len(item.content) > 50 else ''}")
            print(f"   📅 Created: {item.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   📍 Device: {item.source_device}")
            print(f"   🏷️  Tags: {', '.join(item.tags) if item.tags else 'None'}")
            
            if self._contains_yourl_codes(item.content):
                codes = self.yourl_code_pattern.findall(item.content)
                print(f"   🔑 Yourl.Cloud Codes: {', '.join(codes)}")
            
            print(f"   🔗 ID: {item.id[:8]}...")
            print("-" * 40)

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Windows Clipboard History Integration for Yourl.Cloud")
    parser.add_argument("action", nargs='?', choices=["search", "recent", "yourl-codes", "monitor", "display"], 
                       default="display", help="Action to perform")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--tags", nargs="+", help="Tags to filter by")
    parser.add_argument("--hours", type=int, default=24, help="Hours to look back for recent items")
    parser.add_argument("--project-id", default="yourl-cloud", help="Google Cloud project ID")
    parser.add_argument("--bridge-url", default="https://cb.yourl.cloud", help="Clipboard bridge URL")
    
    args = parser.parse_args()
    
    try:
        # Initialize clipboard history
        clipboard_history = WindowsClipboardHistory(
            project_id=args.project_id,
            clipboard_bridge_url=args.bridge_url
        )
        
        if args.action == "search":
            items = clipboard_history.search_clipboard_history(query=args.query, tags=args.tags)
            clipboard_history.display_history(items)
        
        elif args.action == "recent":
            items = clipboard_history.get_recent_items(hours=args.hours)
            clipboard_history.display_history(items)
        
        elif args.action == "yourl-codes":
            items = clipboard_history.get_yourl_codes_from_history()
            clipboard_history.display_history(items)
        
        elif args.action == "monitor":
            print("Starting clipboard monitoring... Press Ctrl+C to stop")
            clipboard_history.start_monitoring()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                clipboard_history.stop_monitoring()
                print("\nStopped clipboard monitoring")
        
        elif args.action == "display":
            clipboard_history.display_history()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
