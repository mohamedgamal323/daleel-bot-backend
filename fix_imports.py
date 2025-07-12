#!/usr/bin/env python3
"""
Script to fix import paths after monorepo restructuring
"""

import os
import re
from pathlib import Path

# Define the root directory
root_dir = Path("/mnt/84E663DCE663CCCC/Work/personal-projects/daleel-bot/daleel-bot-backend")

# Define import replacements
replacements = {
    r"from src\.application": "from src.backend.application",
    r"from src\.domain": "from src.backend.domain", 
    r"from src\.infrastructure": "from src.backend.infrastructure",
    r"from src\.infrastructure_persistence": "from src.backend.infrastructure_persistence",
    r"from src\.infrastructure_integration": "from src.backend.infrastructure_integration",
    r"from src\.infrastructure_vectordb": "from src.backend.infrastructure_vectordb",
    r"from src\.common": "from src.backend.common",
    r"from src\.api": "from src.backend.api",
    r"from src\.main": "from src.backend.main",
}

def fix_file(file_path):
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

def main():
    # Find all Python files in the backend directory
    backend_dir = root_dir / "src" / "backend"
    
    for python_file in backend_dir.rglob("*.py"):
        fix_file(python_file)
    
    print("Import fixing completed!")

if __name__ == "__main__":
    main()
