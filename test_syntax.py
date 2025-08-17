#!/usr/bin/env python3
"""Test script to debug syntax issues"""

try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"File size: {len(content)} characters")
    print(f"Number of lines: {len(content.splitlines())}")
    
    # Try to compile the code
    import ast
    try:
        ast.parse(content)
        print("✅ AST parsing successful")
    except SyntaxError as e:
        print(f"❌ AST parsing failed: {e}")
        print(f"Error at line {e.lineno}, column {e.offset}")
        if e.lineno:
            lines = content.splitlines()
            if e.lineno <= len(lines):
                print(f"Problematic line: {lines[e.lineno-1]}")
    
    # Try to compile as bytecode
    try:
        compile(content, 'app.py', 'exec')
        print("✅ Bytecode compilation successful")
    except SyntaxError as e:
        print(f"❌ Bytecode compilation failed: {e}")
        print(f"Error at line {e.lineno}, column {e.offset}")
        if e.lineno:
            lines = content.splitlines()
            if e.lineno <= len(lines):
                print(f"Problematic line: {lines[e.lineno-1]}")
                # Show context around the error
                for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
                    marker = ">>> " if i == e.lineno-1 else "    "
                    print(f"{marker}{i+1:4d}: {lines[i]}")

except Exception as e:
    print(f"Failed to read file: {e}")

