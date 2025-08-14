#!/usr/bin/env python3
"""
Test Local Clipboard History - Standalone Offline Instance
=========================================================

This script provides a standalone test environment for Windows clipboard history
integration that can be run from IDE terminals without requiring the full
Yourl.Cloud infrastructure.

Features:
- Offline clipboard history testing
- Local storage only (no cloud sync)
- Mock Yourl.Cloud code detection
- Test data generation
- IDE-friendly output

Author: Yourl.Cloud Inc.
Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
Environment: Local Test
"""

import os
import sys
import json
import time
import hashlib
import threading
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging
import re
import random
import string

# Configure logging for IDE terminals
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('clipboard_test.log')
    ]
)
logger = logging.getLogger('test_clipboard_history')

@dataclass
class TestClipboardItem:
    """Represents a test clipboard item for local testing"""
    id: str
    content: str
    content_type: str  # 'text', 'image', 'file'
    source_device: str
    created_at: datetime
    accessed_at: datetime
    tags: List[str]
    metadata: Dict[str, Any]
    is_test_data: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/transmission"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['accessed_at'] = self.accessed_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestClipboardItem':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['accessed_at'] = datetime.fromisoformat(data['accessed_at'])
        return cls(**data)

class TestClipboardHistory:
    """Test clipboard history for local development and testing"""
    
    def __init__(self, test_mode: bool = True):
        self.test_mode = test_mode
        self.history_items: Dict[str, TestClipboardItem] = {}
        self.yourl_code_pattern = re.compile(r'\b[A-Z]{4,8}\d{2,3}[!@#$%^&*+=?~]\b')
        self.device_id = self._get_device_id()
        self.test_data_generated = False
        
        # Load existing history or generate test data
        self._load_history()
        if not self.history_items and test_mode:
            self._generate_test_data()
    
    def _get_device_id(self) -> str:
        """Get unique device identifier for testing"""
        try:
            hostname = os.environ.get('COMPUTERNAME', 'test-device')
            username = os.environ.get('USERNAME', 'test-user')
            return f"{hostname}-{username}-test"
        except Exception as e:
            logger.error(f"Failed to get device ID: {e}")
            return "test-device"
    
    def _load_history(self):
        """Load clipboard history from local storage"""
        try:
            history_file = os.path.expanduser("~/.test_clipboard_history.json")
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    for item_data in data.get('items', []):
                        item = TestClipboardItem.from_dict(item_data)
                        self.history_items[item.id] = item
                logger.info(f"Loaded {len(self.history_items)} test clipboard items")
        except Exception as e:
            logger.error(f"Failed to load test clipboard history: {e}")
    
    def _save_history(self):
        """Save clipboard history to local storage"""
        try:
            history_file = os.path.expanduser("~/.test_clipboard_history.json")
            data = {
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'device_id': self.device_id,
                'test_mode': self.test_mode,
                'items': [item.to_dict() for item in self.history_items.values()]
            }
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save test clipboard history: {e}")
    
    def _generate_test_data(self):
        """Generate test clipboard data for local testing"""
        if self.test_data_generated:
            return
        
        logger.info("Generating test clipboard data...")
        
        # Test Yourl.Cloud codes
        test_codes = [
            "CLOUD123!",
            "FUTURE456@",
            "INNOVATE789#",
            "TRUST2024$",
            "FAMILY999%"
        ]
        
        # Test content samples
        test_contents = [
            "Yourl.Cloud code: CLOUD123! - Use this for testing",
            "Important note: FUTURE456@ is the latest code",
            "Meeting reminder: INNOVATE789# expires tomorrow",
            "Emergency contact: TRUST2024$ for family access",
            "Test content without any codes",
            "https://cb.yourl.cloud - Clipboard bridge URL",
            "Email: test@yourl.cloud for support",
            "Phone: 555-123-4567 for urgent matters",
            f"Test clipboard item {random.randint(1000, 9999)}",
            "This is a sample clipboard content for testing purposes"
        ]
        
        # Generate test items
        for i, content in enumerate(test_contents):
            item_id = self._generate_item_id(content)
            created_at = datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 72))
            accessed_at = created_at + timedelta(minutes=random.randint(1, 60))
            
            item = TestClipboardItem(
                id=item_id,
                content=content,
                content_type='text',
                source_device=self.device_id,
                created_at=created_at,
                accessed_at=accessed_at,
                tags=self._extract_tags(content),
                metadata=self._extract_metadata(content),
                is_test_data=True
            )
            
            self.history_items[item_id] = item
        
        self._save_history()
        self.test_data_generated = True
        logger.info(f"Generated {len(self.history_items)} test clipboard items")
    
    def _generate_item_id(self, content: str) -> str:
        """Generate unique ID for clipboard item"""
        unique_string = f"{content[:50]}{self.device_id}{time.time()}{random.random()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
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
        
        # Add test tag
        tags.append('test-data')
        
        return tags
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from clipboard content"""
        metadata = {
            'length': len(content),
            'has_yourl_codes': self._contains_yourl_codes(content),
            'content_preview': content[:100] + '...' if len(content) > 100 else content,
            'test_mode': True
        }
        
        # Extract Yourl.Cloud codes if present
        if self._contains_yourl_codes(content):
            codes = self.yourl_code_pattern.findall(content)
            metadata['yourl_codes'] = codes
        
        return metadata
    
    def _contains_yourl_codes(self, content: str) -> bool:
        """Check if content contains Yourl.Cloud codes"""
        return bool(self.yourl_code_pattern.search(content))
    
    def add_test_item(self, content: str, content_type: str = 'text') -> Optional[TestClipboardItem]:
        """Add a new test clipboard item"""
        try:
            # Generate unique ID
            item_id = self._generate_item_id(content)
            
            # Check if item already exists
            for existing_item in self.history_items.values():
                if existing_item.content == content:
                    existing_item.accessed_at = datetime.now(timezone.utc)
                    self._save_history()
                    return existing_item
            
            # Create new item
            item = TestClipboardItem(
                id=item_id,
                content=content,
                content_type=content_type,
                source_device=self.device_id,
                created_at=datetime.now(timezone.utc),
                accessed_at=datetime.now(timezone.utc),
                tags=self._extract_tags(content),
                metadata=self._extract_metadata(content),
                is_test_data=True
            )
            
            # Add to history
            self.history_items[item_id] = item
            self._save_history()
            
            logger.info(f"Added test clipboard item: {item_id[:8]}...")
            return item
            
        except Exception as e:
            logger.error(f"Failed to add test clipboard item: {e}")
            return None
    
    def search_clipboard_history(self, query: Optional[str] = None, tags: Optional[List[str]] = None, 
                                include_yourl_codes: bool = True) -> List[TestClipboardItem]:
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
    
    def get_yourl_codes_from_history(self) -> List[TestClipboardItem]:
        """Get all clipboard items containing Yourl.Cloud codes"""
        return self.search_clipboard_history(include_yourl_codes=True)
    
    def get_recent_items(self, hours: int = 24) -> List[TestClipboardItem]:
        """Get recent clipboard items"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        recent_items = []
        
        for item in self.history_items.values():
            if item.accessed_at >= cutoff_time:
                recent_items.append(item)
        
        # Sort by access time (most recent first)
        recent_items.sort(key=lambda x: x.accessed_at, reverse=True)
        
        return recent_items
    
    def display_history(self, items: Optional[List[TestClipboardItem]] = None, 
                       show_yourl_codes_only: bool = False):
        """Display clipboard history in a formatted way for IDE terminals"""
        if items is None:
            if show_yourl_codes_only:
                items = self.get_yourl_codes_from_history()
            else:
                items = self.get_recent_items()
        
        if not items:
            print("No clipboard items found.")
            return
        
        print(f"\n📋 Test Clipboard History ({len(items)} items)")
        print("=" * 80)
        print(f"🔧 Test Mode: {self.test_mode}")
        print(f"📍 Device: {self.device_id}")
        print(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
            if item.is_test_data:
                print(f"   🧪 Test Data: Yes")
            print("-" * 40)
    
    def clear_test_data(self):
        """Clear all test data"""
        self.history_items.clear()
        self._save_history()
        logger.info("Cleared all test clipboard data")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the clipboard history"""
        total_items = len(self.history_items)
        yourl_code_items = len(self.get_yourl_codes_from_history())
        recent_items = len(self.get_recent_items(24))
        
        # Count by tags
        tag_counts = {}
        for item in self.history_items.values():
            for tag in item.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            'total_items': total_items,
            'yourl_code_items': yourl_code_items,
            'recent_items_24h': recent_items,
            'tag_counts': tag_counts,
            'test_mode': self.test_mode,
            'device_id': self.device_id
        }

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Local Clipboard History - Standalone Offline Instance")
    parser.add_argument("action", nargs='?', choices=["search", "recent", "yourl-codes", "display", "stats", "clear", "add"], 
                       default="display", help="Action to perform")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--tags", nargs="+", help="Tags to filter by")
    parser.add_argument("--hours", type=int, default=24, help="Hours to look back for recent items")
    parser.add_argument("--content", help="Content to add (for add action)")
    parser.add_argument("--test-mode", action="store_true", default=True, help="Run in test mode")
    
    args = parser.parse_args()
    
    try:
        # Initialize test clipboard history
        clipboard_history = TestClipboardHistory(test_mode=args.test_mode)
        
        if args.action == "search":
            items = clipboard_history.search_clipboard_history(query=args.query, tags=args.tags)
            clipboard_history.display_history(items)
        
        elif args.action == "recent":
            items = clipboard_history.get_recent_items(hours=args.hours)
            clipboard_history.display_history(items)
        
        elif args.action == "yourl-codes":
            items = clipboard_history.get_yourl_codes_from_history()
            clipboard_history.display_history(items)
        
        elif args.action == "display":
            clipboard_history.display_history()
        
        elif args.action == "stats":
            stats = clipboard_history.get_statistics()
            print("\n📊 Test Clipboard History Statistics")
            print("=" * 50)
            for key, value in stats.items():
                print(f"{key}: {value}")
        
        elif args.action == "clear":
            confirm = input("Are you sure you want to clear all test data? (y/n): ")
            if confirm.lower() == 'y':
                clipboard_history.clear_test_data()
                print("Test data cleared successfully.")
            else:
                print("Operation cancelled.")
        
        elif args.action == "add":
            if args.content:
                item = clipboard_history.add_test_item(args.content)
                if item:
                    print(f"Added test item: {item.content[:50]}...")
                else:
                    print("Failed to add test item.")
            else:
                print("Please provide content with --content parameter.")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

