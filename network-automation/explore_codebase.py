#!/usr/bin/env python3
"""
Script to explore and understand the NornFlow codebase structure.
Run this from the root of your nornflow-netops repository.
"""

import os
import sys
from pathlib import Path


def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """Print directory tree structure."""
    if current_depth >= max_depth:
        return
    
    directory = Path(directory)
    if not directory.exists():
        return
    
    items = sorted([item for item in directory.iterdir() 
                   if not item.name.startswith('.') and item.name != '__pycache__'])
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and current_depth < max_depth - 1:
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension, max_depth, current_depth + 1)


def analyze_python_files(directory):
    """Analyze Python files to understand the codebase."""
    directory = Path(directory)
    python_files = list(directory.rglob("*.py"))
    
    print(f"\n📊 Python Files Analysis")
    print(f"Total Python files: {len(python_files)}")
    
    # Categorize files
    categories = {
        "Core": [],
        "CLI": [],
        "Built-ins": [],
        "Tests": [],
        "Other": []
    }
    
    for file in python_files:
        rel_path = file.relative_to(directory)
        if "cli" in str(rel_path):
            categories["CLI"].append(rel_path)
        elif "builtins" in str(rel_path):
            categories["Built-ins"].append(rel_path)
        elif "test" in str(rel_path):
            categories["Tests"].append(rel_path)
        elif str(rel_path).startswith("nornflow/"):
            categories["Core"].append(rel_path)
        else:
            categories["Other"].append(rel_path)
    
    for category, files in categories.items():
        if files:
            print(f"\n{category} ({len(files)} files):")
            for file in sorted(files):
                print(f"  - {file}")


def check_dependencies():
    """Check project dependencies."""
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        print(f"\n📦 Dependencies (from pyproject.toml)")
        with open(pyproject_path) as f:
            content = f.read()
            
        # Extract dependencies section
        in_deps = False
        deps = []
        for line in content.split('\n'):
            if line.strip() == 'dependencies = [':
                in_deps = True
                continue
            elif in_deps and line.strip() == ']':
                break
            elif in_deps and line.strip():
                deps.append(line.strip().strip('",'))
        
        print("Main dependencies:")
        for dep in deps:
            if dep:
                print(f"  - {dep}")


def main():
    """Main exploration function."""
    print("🔍 NornFlow Codebase Explorer")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("nornflow").exists():
        print("❌ Error: nornflow directory not found.")
        print("Make sure you're running this from the root of the nornflow-netops repository.")
        sys.exit(1)
    
    print("\n📁 Project Structure:")
    print_tree(".", max_depth=3)
    
    analyze_python_files(".")
    check_dependencies()
    
    print(f"\n🎯 Key Areas for Enhancement:")
    print("1. nornflow/builtins/tasks.py - Current built-in tasks (set, echo, write_file)")
    print("2. nornflow/builtins/filters.py - Current filters (hosts, groups)")
    print("3. nornflow/workflow.py - Workflow execution engine")
    print("4. nornflow/catalogs.py - Task/workflow/filter discovery")
    print("5. nornflow/cli/ - Command-line interface")
    
    print(f"\n📋 Next Steps:")
    print("1. Examine the built-in tasks to understand the task interface")
    print("2. Look at workflow.py to understand execution flow")
    print("3. Create our network automation task library")
    print("4. Add advanced workflow control features")


if __name__ == "__main__":
    main()
