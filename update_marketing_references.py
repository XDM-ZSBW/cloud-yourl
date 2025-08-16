#!/usr/bin/env python3
"""
Script to update all remaining marketing password references to marketing code
"""

import re

def update_file(file_path):
    """Update marketing password references in a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update function calls
    content = re.sub(r'get_current_marketing_password\(\)', 'get_current_marketing_code()', content)
    content = re.sub(r'get_next_marketing_password\(\)', 'get_next_marketing_code()', content)
    content = re.sub(r'generate_marketing_password\(\)', 'generate_marketing_code()', content)
    content = re.sub(r'generate_marketing_password_from_hash\(', 'generate_marketing_code_from_hash(', content)
    
    # Update variable names and comments
    content = re.sub(r'BUILD_MARKETING_PASSWORD', 'BUILD_MARKETING_CODE', content)
    content = re.sub(r'current_marketing_password', 'current_marketing_code', content)
    content = re.sub(r'next_marketing_password', 'next_marketing_code', content)
    
    # Update comments
    content = re.sub(r'# Get current marketing password', '# Get current marketing code', content)
    content = re.sub(r'# Get next marketing password', '# Get next marketing code', content)
    content = re.sub(r'Get the current live marketing password', 'Get the current live marketing code', content)
    content = re.sub(r'Get the next marketing password', 'Get the next marketing code', content)
    content = re.sub(r'Generate marketing password from specific commit hash', 'Generate marketing code from specific commit hash', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")

if __name__ == "__main__":
    update_file("app.py")
    print("All marketing password references updated to marketing code!")
