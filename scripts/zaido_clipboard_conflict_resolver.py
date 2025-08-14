#!/usr/bin/env python3
"""
Zaido Clipboard Conflict Resolver - Yourl.Cloud Code Recovery
============================================================

This script helps resolve clipboard conflicts with the Zaido browser extension
and specifically helps you find Yourl.Cloud codes that may have been overwritten
by screenshots or other clipboard content.

Features:
- Detects Zaido extension clipboard conflicts
- Recovers Yourl.Cloud codes from clipboard history
- Provides alternative code recovery methods
- Works with Windows clipboard history (Win+V)
- Integrates with Yourl.Cloud clipboard bridge

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Environment: Zaido Extension Conflict Resolution
"""

import os
import sys
import json
import time
import hashlib
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging
import re
import subprocess
import win32clipboard
import win32con

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('zaido_conflict_resolver')

@dataclass
class ClipboardConflictItem:
    """Represents a clipboard item that may have been overwritten by Zaido"""
    id: str
    content: str
    content_type: str  # 'text', 'image', 'screenshot'
    source: str  # 'zaido', 'windows', 'yourl-cloud'
    created_at: datetime
    accessed_at: datetime
    tags: List[str]
    metadata: Dict[str, Any]
    is_conflict: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/transmission"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['accessed_at'] = self.accessed_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClipboardConflictItem':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['accessed_at'] = datetime.fromisoformat(data['accessed_at'])
        return cls(**data)

class ZaidoConflictResolver:
    """Resolves clipboard conflicts with Zaido extension"""
    
    def __init__(self, clipboard_bridge_url: str = 'https://cb.yourl.cloud'):
        self.clipboard_bridge_url = clipboard_bridge_url
        self.yourl_code_pattern = re.compile(r'\b[A-Z]{4,8}\d{2,3}[!@#$%^&*+=?~]\b')
        self.device_id = self._get_device_id()
        self.conflict_items: Dict[str, ClipboardConflictItem] = {}
        
        # Load existing conflict history
        self._load_conflict_history()
    
    def _get_device_id(self) -> str:
        """Get unique device identifier"""
        try:
            hostname = os.environ.get('COMPUTERNAME', 'unknown')
            username = os.environ.get('USERNAME', 'unknown')
            return f"{hostname}-{username}"
        except Exception as e:
            logger.error(f"Failed to get device ID: {e}")
            return "unknown-device"
    
    def _load_conflict_history(self):
        """Load conflict history from local storage"""
        try:
            history_file = os.path.expanduser("~/.zaido_conflict_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    for item_data in data.get('items', []):
                        item = ClipboardConflictItem.from_dict(item_data)
                        self.conflict_items[item.id] = item
                logger.info(f"Loaded {len(self.conflict_items)} conflict items")
        except Exception as e:
            logger.error(f"Failed to load conflict history: {e}")
    
    def _save_conflict_history(self):
        """Save conflict history to local storage"""
        try:
            history_file = os.path.expanduser("~/.zaido_conflict_history.json")
            data = {
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'device_id': self.device_id,
                'items': [item.to_dict() for item in self.conflict_items.values()]
            }
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save conflict history: {e}")
    
    def detect_zaido_conflict(self) -> bool:
        """Detect if Zaido extension is causing clipboard conflicts"""
        try:
            # Check if Zaido extension is active
            zaido_processes = self._check_zaido_processes()
            if zaido_processes:
                logger.info(f"Found {len(zaido_processes)} Zaido processes")
                return True
            
            # Check clipboard content for Zaido signatures
            clipboard_content = self._get_clipboard_content()
            if clipboard_content and self._is_zaido_content(clipboard_content):
                logger.info("Detected Zaido content in clipboard")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error detecting Zaido conflict: {e}")
            return False
    
    def _check_zaido_processes(self) -> List[str]:
        """Check for running Zaido processes"""
        try:
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq *zaido*'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0 and 'zaido' in result.stdout.lower():
                return [line for line in result.stdout.split('\n') if 'zaido' in line.lower()]
        except Exception as e:
            logger.error(f"Error checking Zaido processes: {e}")
        return []
    
    def _get_clipboard_content(self) -> Optional[str]:
        """Get current clipboard content"""
        try:
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                    content = win32clipboard.GetClipboardData(win32con.CF_TEXT)
                    if isinstance(content, bytes):
                        return content.decode('utf-8', errors='ignore')
                    return content
            finally:
                win32clipboard.CloseClipboard()
        except Exception as e:
            logger.error(f"Error getting clipboard content: {e}")
        return None
    
    def _is_zaido_content(self, content: str) -> bool:
        """Check if content is from Zaido extension"""
        zaido_indicators = [
            'zaido',
            'screenshot',
            'capture',
            'data:image',
            'base64',
            'yourl.cloud'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in zaido_indicators)
    
    def recover_yourl_codes(self) -> List[str]:
        """Recover Yourl.Cloud codes from various sources"""
        recovered_codes = []
        
        # 1. Check current clipboard
        clipboard_content = self._get_clipboard_content()
        if clipboard_content:
            codes = self.yourl_code_pattern.findall(clipboard_content)
            recovered_codes.extend(codes)
        
        # 2. Check Windows clipboard history (Win+V)
        windows_history_codes = self._check_windows_clipboard_history()
        recovered_codes.extend(windows_history_codes)
        
        # 3. Check Yourl.Cloud clipboard bridge
        bridge_codes = self._check_clipboard_bridge()
        recovered_codes.extend(bridge_codes)
        
        # 4. Check local conflict history
        history_codes = self._check_conflict_history()
        recovered_codes.extend(history_codes)
        
        # Remove duplicates and return
        return list(set(recovered_codes))
    
    def _check_windows_clipboard_history(self) -> List[str]:
        """Check Windows clipboard history for Yourl.Cloud codes"""
        codes = []
        try:
            # This would require Windows clipboard history API
            # For now, we'll check the local storage
            history_file = os.path.expanduser("~/.yourl_clipboard_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    for item in data.get('items', []):
                        content = item.get('content', '')
                        found_codes = self.yourl_code_pattern.findall(content)
                        codes.extend(found_codes)
        except Exception as e:
            logger.error(f"Error checking Windows clipboard history: {e}")
        return codes
    
    def _check_clipboard_bridge(self) -> List[str]:
        """Check Yourl.Cloud clipboard bridge for codes"""
        codes = []
        try:
            response = requests.get(f"{self.clipboard_bridge_url}/api/clipboard/all-devices", timeout=10)
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    content = item.get('content', '')
                    found_codes = self.yourl_code_pattern.findall(content)
                    codes.extend(found_codes)
        except Exception as e:
            logger.error(f"Error checking clipboard bridge: {e}")
        return codes
    
    def _check_conflict_history(self) -> List[str]:
        """Check local conflict history for codes"""
        codes = []
        for item in self.conflict_items.values():
            found_codes = self.yourl_code_pattern.findall(item.content)
            codes.extend(found_codes)
        return codes
    
    def add_conflict_item(self, content: str, content_type: str = 'text', source: str = 'unknown'):
        """Add a new conflict item"""
        try:
            item_id = hashlib.sha256(f"{content[:50]}{time.time()}".encode()).hexdigest()[:16]
            
            item = ClipboardConflictItem(
                id=item_id,
                content=content,
                content_type=content_type,
                source=source,
                created_at=datetime.now(timezone.utc),
                accessed_at=datetime.now(timezone.utc),
                tags=self._extract_tags(content),
                metadata=self._extract_metadata(content),
                is_conflict=True
            )
            
            self.conflict_items[item_id] = item
            self._save_conflict_history()
            
            logger.info(f"Added conflict item: {item_id[:8]}...")
            return item
            
        except Exception as e:
            logger.error(f"Failed to add conflict item: {e}")
            return None
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content"""
        tags = []
        
        if self._contains_yourl_codes(content):
            tags.append('yourl-cloud-code')
        
        if self._is_zaido_content(content):
            tags.append('zaido-content')
        
        if 'screenshot' in content.lower():
            tags.append('screenshot')
        
        if 'image' in content.lower():
            tags.append('image')
        
        return tags
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from content"""
        metadata = {
            'length': len(content),
            'has_yourl_codes': self._contains_yourl_codes(content),
            'is_zaido_content': self._is_zaido_content(content),
            'content_preview': content[:100] + '...' if len(content) > 100 else content
        }
        
        if self._contains_yourl_codes(content):
            codes = self.yourl_code_pattern.findall(content)
            metadata['yourl_codes'] = codes
        
        return metadata
    
    def _contains_yourl_codes(self, content: str) -> bool:
        """Check if content contains Yourl.Cloud codes"""
        return bool(self.yourl_code_pattern.search(content))
    
    def display_recovery_results(self, codes: List[str]):
        """Display recovery results in a formatted way"""
        if not codes:
            print("\n❌ No Yourl.Cloud codes found in clipboard history.")
            print("\n🔍 Try these recovery methods:")
            print("   1. Check Windows clipboard history (Win+V)")
            print("   2. Look in your browser history")
            print("   3. Check your notes or documents")
            print("   4. Use the Zaido extension to search for codes")
            return
        
        print(f"\n✅ Found {len(codes)} Yourl.Cloud code(s):")
        print("=" * 50)
        
        for i, code in enumerate(codes, 1):
            print(f"{i}. {code}")
        
        print("\n📋 Recovery Summary:")
        print(f"   • Total codes found: {len(codes)}")
        print(f"   • Device: {self.device_id}")
        print(f"   • Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n💡 Tips to avoid future conflicts:")
        print("   • Use Ctrl+Shift+V to paste without formatting")
        print("   • Check clipboard history before pasting")
        print("   • Use the Zaido extension's search feature")
        print("   • Keep codes in a separate text file")
    
    def resolve_conflict(self) -> bool:
        """Main method to resolve Zaido clipboard conflicts"""
        print("\n🔍 Zaido Clipboard Conflict Resolver")
        print("=" * 50)
        
        # Detect conflict
        if self.detect_zaido_conflict():
            print("⚠️  Zaido extension conflict detected!")
            print("   • Zaido extension may have overwritten your clipboard")
            print("   • Attempting to recover Yourl.Cloud codes...")
        else:
            print("✅ No Zaido conflicts detected")
        
        # Recover codes
        recovered_codes = self.recover_yourl_codes()
        self.display_recovery_results(recovered_codes)
        
        return len(recovered_codes) > 0

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Zaido Clipboard Conflict Resolver")
    parser.add_argument("action", nargs='?', choices=["resolve", "recover", "detect", "history"], 
                       default="resolve", help="Action to perform")
    parser.add_argument("--bridge-url", default="https://cb.yourl.cloud", help="Clipboard bridge URL")
    
    args = parser.parse_args()
    
    try:
        resolver = ZaidoConflictResolver(clipboard_bridge_url=args.bridge_url)
        
        if args.action == "resolve":
            success = resolver.resolve_conflict()
            if not success:
                print("\n💡 Additional recovery suggestions:")
                print("   • Check your browser's clipboard history")
                print("   • Look in your recent documents")
                print("   • Search your email for the code")
                print("   • Check your phone's clipboard")
        
        elif args.action == "recover":
            codes = resolver.recover_yourl_codes()
            resolver.display_recovery_results(codes)
        
        elif args.action == "detect":
            if resolver.detect_zaido_conflict():
                print("⚠️  Zaido extension conflict detected!")
            else:
                print("✅ No Zaido conflicts detected")
        
        elif args.action == "history":
            print(f"\n📋 Conflict History ({len(resolver.conflict_items)} items)")
            for item in resolver.conflict_items.values():
                print(f"   • {item.content[:50]}... ({item.source})")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
