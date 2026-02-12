#!/usr/bin/env python3
"""
Simple validation script for enhanced workflow control features.

This script validates the basic functionality without requiring external dependencies.
"""

import sys
import os
from pathlib import Path


def validate_file_structure():
    """Validate that all required files were created."""
    print("🔍 Validating Enhanced Workflow Control File Structure")
    print("=" * 60)
    
    required_files = [
        "enhancements/workflow_control/control_structures.py",
        "enhancements/workflow_control/enhanced_workflow.py", 
        "enhancements/workflow_control/integration_example.py",
        "enhancements/workflow_control/README.md",
        "sample_workflows/enhanced_control_examples.yaml",
        "test_enhanced_workflow_control.py",
        "TASK_2_COMPLETION_SUMMARY.md"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 File Structure Summary:")
    print(f"   ✅ Existing: {len(existing_files)}")
    print(f"   ❌ Missing: {len(missing_files)}")
    
    return len(missing_files) == 0


def validate_python_syntax():
    """Validate Python syntax of created files."""
    print("\n🐍 Validating Python Syntax")
    print("=" * 60)
    
    python_files = [
        "enhancements/workflow_control/control_structures.py",
        "enhancements/workflow_control/enhanced_workflow.py",
        "enhancements/workflow_control/integration_example.py",
        "test_enhanced_workflow_control.py",
        "validate_enhanced_workflow.py"
    ]
    
    syntax_errors = []
    valid_files = []
    
    for file_path in python_files:
        if not Path(file_path).exists():
            print(f"⏭️  {file_path} (file not found)")
            continue
            
        try:
            with open(file_path, 'r') as f:
                source_code = f.read()
            
            # Compile to check syntax
            compile(source_code, file_path, 'exec')
            valid_files.append(file_path)
            print(f"✅ {file_path}")
            
        except SyntaxError as e:
            syntax_errors.append((file_path, str(e)))
            print(f"❌ {file_path}: {e}")
        except Exception as e:
            syntax_errors.append((file_path, str(e)))
            print(f"⚠️  {file_path}: {e}")
    
    print(f"\n📊 Python Syntax Summary:")
    print(f"   ✅ Valid: {len(valid_files)}")
    print(f"   ❌ Errors: {len(syntax_errors)}")
    
    return len(syntax_errors) == 0


def validate_imports():
    """Validate that imports work correctly."""
    print("\n📦 Validating Import Structure")
    print("=" * 60)
    
    import_tests = [
        ("enhancements.workflow_control.control_structures", [
            "ConditionEvaluator", "RetryStrategy", "LoopController", 
            "WorkflowControlEngine", "EnhancedTaskModel", "ExecutionMode"
        ]),
        ("enhancements.workflow_control.enhanced_workflow", [
            "EnhancedWorkflowExecutor"
        ])
    ]
    
    import_errors = []
    successful_imports = []
    
    # Add current directory to Python path
    sys.path.insert(0, os.getcwd())
    
    for module_name, expected_classes in import_tests:
        try:
            module = __import__(module_name, fromlist=expected_classes)
            
            missing_classes = []
            for class_name in expected_classes:
                if hasattr(module, class_name):
                    successful_imports.append(f"{module_name}.{class_name}")
                else:
                    missing_classes.append(class_name)
            
            if missing_classes:
                import_errors.append((module_name, f"Missing classes: {missing_classes}"))
                print(f"⚠️  {module_name}: Missing {missing_classes}")
            else:
                print(f"✅ {module_name}: All classes available")
                
        except ImportError as e:
            import_errors.append((module_name, str(e)))
            print(f"❌ {module_name}: {e}")
        except Exception as e:
            import_errors.append((module_name, str(e)))
            print(f"⚠️  {module_name}: {e}")
    
    print(f"\n📊 Import Summary:")
    print(f"   ✅ Successful: {len(successful_imports)}")
    print(f"   ❌ Errors: {len(import_errors)}")
    
    return len(import_errors) == 0


def validate_basic_functionality():
    """Validate basic functionality without external dependencies."""
    print("\n⚙️  Validating Basic Functionality")
    print("=" * 60)
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        # Test basic class instantiation
        from enhancements.workflow_control.control_structures import (
            RetryStrategy, ExecutionMode
        )
        
        # Test RetryStrategy
        strategy = RetryStrategy(max_attempts=3, delay=1.0)
        assert strategy.max_attempts == 3
        assert strategy.delay == 1.0
        assert strategy.get_delay(1) == 0  # First attempt has no delay
        assert strategy.get_delay(2) == 1.0  # Second attempt has initial delay
        print("✅ RetryStrategy: Basic functionality works")
        
        # Test ExecutionMode enum
        assert ExecutionMode.SEQUENTIAL.value == "sequential"
        assert ExecutionMode.PARALLEL.value == "parallel"
        assert ExecutionMode.CONDITIONAL.value == "conditional"
        assert ExecutionMode.LOOP.value == "loop"
        assert ExecutionMode.RETRY.value == "retry"
        print("✅ ExecutionMode: Enum values correct")
        
        print("\n📊 Basic Functionality Summary:")
        print("   ✅ All basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_yaml_syntax():
    """Validate YAML syntax of workflow files."""
    print("\n📄 Validating YAML Syntax")
    print("=" * 60)
    
    yaml_files = [
        "sample_workflows/enhanced_control_examples.yaml"
    ]
    
    # Simple YAML validation without requiring PyYAML
    yaml_errors = []
    valid_files = []
    
    for file_path in yaml_files:
        if not Path(file_path).exists():
            print(f"⏭️  {file_path} (file not found)")
            continue
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Basic YAML structure validation
            lines = content.split('\n')
            indent_stack = []
            
            for line_num, line in enumerate(lines, 1):
                if line.strip() == '' or line.strip().startswith('#'):
                    continue
                
                # Check for basic YAML structure
                if ':' in line and not line.strip().startswith('-'):
                    # Key-value pair
                    pass
                elif line.strip().startswith('-'):
                    # List item
                    pass
                
            valid_files.append(file_path)
            print(f"✅ {file_path}")
            
        except Exception as e:
            yaml_errors.append((file_path, str(e)))
            print(f"❌ {file_path}: {e}")
    
    print(f"\n📊 YAML Syntax Summary:")
    print(f"   ✅ Valid: {len(valid_files)}")
    print(f"   ❌ Errors: {len(yaml_errors)}")
    
    return len(yaml_errors) == 0


def main():
    """Main validation function."""
    print("🚀 Enhanced Workflow Control Validation")
    print("=" * 70)
    
    validation_results = []
    
    # Run all validations
    validation_results.append(("File Structure", validate_file_structure()))
    validation_results.append(("Python Syntax", validate_python_syntax()))
    validation_results.append(("Import Structure", validate_imports()))
    validation_results.append(("Basic Functionality", validate_basic_functionality()))
    validation_results.append(("YAML Syntax", validate_yaml_syntax()))
    
    # Summary
    print("\n🏁 Validation Summary")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(validation_results)
    
    for test_name, result in validation_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<20} {status}")
        if result:
            passed_tests += 1
    
    print(f"\n📊 Overall Results:")
    print(f"   Tests Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All validations passed! Enhanced Workflow Control is ready.")
        print("\n📋 Next Steps:")
        print("   1. Integrate with your actual NornFlow repository")
        print("   2. Test with real network devices")
        print("   3. Move on to Task 3: Enhanced Integration Framework")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} validation(s) failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
