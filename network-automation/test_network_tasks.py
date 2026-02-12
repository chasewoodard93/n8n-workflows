#!/usr/bin/env python3
"""
Test script for the enhanced network automation tasks.
This script validates that our new tasks are properly structured and importable.
"""

import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, List


def test_task_imports():
    """Test that all network tasks can be imported successfully."""
    print("🧪 Testing Network Task Imports")
    print("=" * 40)
    
    task_modules = [
        "enhancements/network_tasks/device_interaction/connection_tasks.py",
        "enhancements/network_tasks/configuration/config_tasks.py",
        "enhancements/network_tasks/discovery/discovery_tasks.py"
    ]
    
    results = []
    
    for module_path in task_modules:
        try:
            # Load module dynamically
            spec = importlib.util.spec_from_file_location("test_module", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get all functions from the module
            functions = [name for name in dir(module) if callable(getattr(module, name)) and not name.startswith('_')]
            
            results.append({
                "module": module_path,
                "status": "✅ SUCCESS",
                "functions": functions,
                "error": None
            })
            
            print(f"✅ {module_path}")
            print(f"   Functions: {', '.join(functions)}")
            
        except Exception as e:
            results.append({
                "module": module_path,
                "status": "❌ FAILED",
                "functions": [],
                "error": str(e)
            })
            
            print(f"❌ {module_path}")
            print(f"   Error: {str(e)}")
    
    return results


def test_task_signatures():
    """Test that task functions have proper Nornir task signatures."""
    print("\n🔍 Testing Task Signatures")
    print("=" * 40)
    
    # Import the modules
    sys.path.append(".")
    
    try:
        from enhancements.network_tasks.device_interaction.connection_tasks import test_connectivity, execute_command
        from enhancements.network_tasks.configuration.config_tasks import deploy_config, backup_config, validate_config, restore_config
        from enhancements.network_tasks.discovery.discovery_tasks import discover_neighbors, discover_interfaces, discover_device_info
        
        tasks_to_test = [
            ("test_connectivity", test_connectivity),
            ("execute_command", execute_command),
            ("deploy_config", deploy_config),
            ("backup_config", backup_config),
            ("validate_config", validate_config),
            ("restore_config", restore_config),
            ("discover_neighbors", discover_neighbors),
            ("discover_interfaces", discover_interfaces),
            ("discover_device_info", discover_device_info)
        ]
        
        for task_name, task_func in tasks_to_test:
            # Check if function has proper signature
            import inspect
            sig = inspect.signature(task_func)
            params = list(sig.parameters.keys())
            
            if params and params[0] == 'task':
                print(f"✅ {task_name}: Valid signature")
            else:
                print(f"❌ {task_name}: Invalid signature - first parameter should be 'task'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_workflow_syntax():
    """Test that our sample workflow has valid YAML syntax."""
    print("\n📋 Testing Workflow Syntax")
    print("=" * 40)
    
    try:
        import yaml
        
        workflow_file = "sample_workflows/network_operations.yaml"
        
        if not Path(workflow_file).exists():
            print(f"❌ Workflow file not found: {workflow_file}")
            return False
        
        with open(workflow_file, 'r') as f:
            workflow_data = yaml.safe_load(f)
        
        # Basic validation
        if 'workflow' not in workflow_data:
            print("❌ Workflow missing 'workflow' key")
            return False
        
        workflow = workflow_data['workflow']
        
        if 'name' not in workflow:
            print("❌ Workflow missing 'name'")
            return False
        
        if 'tasks' not in workflow:
            print("❌ Workflow missing 'tasks'")
            return False
        
        tasks = workflow['tasks']
        if not isinstance(tasks, list) or len(tasks) == 0:
            print("❌ Workflow tasks should be a non-empty list")
            return False
        
        print(f"✅ Workflow syntax valid")
        print(f"   Name: {workflow['name']}")
        print(f"   Tasks: {len(tasks)}")
        print(f"   Description: {workflow.get('description', 'N/A')}")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing workflow: {e}")
        return False


def test_directory_structure():
    """Test that the enhancement directory structure is correct."""
    print("\n📁 Testing Directory Structure")
    print("=" * 40)
    
    required_dirs = [
        "enhancements",
        "enhancements/network_tasks",
        "enhancements/network_tasks/device_interaction",
        "enhancements/network_tasks/configuration",
        "enhancements/network_tasks/discovery",
        "sample_workflows"
    ]
    
    required_files = [
        "enhancements/network_tasks/README.md",
        "enhancements/network_tasks/device_interaction/connection_tasks.py",
        "enhancements/network_tasks/configuration/config_tasks.py",
        "enhancements/network_tasks/discovery/discovery_tasks.py",
        "sample_workflows/network_operations.yaml"
    ]
    
    all_good = True
    
    # Check directories
    for directory in required_dirs:
        if Path(directory).exists() and Path(directory).is_dir():
            print(f"✅ Directory: {directory}")
        else:
            print(f"❌ Missing directory: {directory}")
            all_good = False
    
    # Check files
    for file_path in required_files:
        if Path(file_path).exists() and Path(file_path).is_file():
            print(f"✅ File: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good


def generate_task_catalog():
    """Generate a catalog of all available network tasks."""
    print("\n📚 Network Task Catalog")
    print("=" * 40)
    
    catalog = {
        "Device Interaction": [
            "test_connectivity - Test network connectivity using ping, TCP, or SSH",
            "execute_command - Execute commands on devices with TextFSM support"
        ],
        "Configuration Management": [
            "deploy_config - Deploy configuration with backup and validation",
            "backup_config - Create timestamped configuration backups",
            "validate_config - Validate configuration with custom checks",
            "restore_config - Restore configuration from backup files"
        ],
        "Network Discovery": [
            "discover_neighbors - Discover neighbors using LLDP/CDP",
            "discover_interfaces - Discover device interfaces and properties",
            "discover_device_info - Comprehensive device information discovery"
        ]
    }
    
    for category, tasks in catalog.items():
        print(f"\n{category}:")
        for task in tasks:
            print(f"  • {task}")
    
    return catalog


def main():
    """Main test function."""
    print("🚀 NornFlow Network Tasks Validation")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Task Imports", test_task_imports),
        ("Task Signatures", test_task_signatures),
        ("Workflow Syntax", test_workflow_syntax)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Generate task catalog
    generate_task_catalog()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your network tasks are ready to use.")
        print("\nNext steps:")
        print("1. Copy the network_tasks directory to your NornFlow project")
        print("2. Update your nornflow.yaml to include the new task directories")
        print("3. Test the sample workflow: nornflow run sample_workflows/network_operations.yaml --dry-run")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues before proceeding.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
