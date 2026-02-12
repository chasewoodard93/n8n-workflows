#!/usr/bin/env python3
"""
Test suite for enhanced workflow control features.

This test suite validates the functionality of the enhanced workflow control
components including conditional execution, loops, error handling, and retry mechanisms.
"""

import pytest
import time
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, Any

# Import the enhanced workflow control components
try:
    from enhancements.workflow_control.control_structures import (
        ConditionEvaluator,
        RetryStrategy,
        LoopController,
        WorkflowControlEngine,
        EnhancedTaskModel,
        parse_enhanced_workflow,
        ExecutionMode
    )
    from enhancements.workflow_control.enhanced_workflow import EnhancedWorkflowExecutor
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import enhanced workflow control modules: {e}")
    IMPORTS_AVAILABLE = False


class TestConditionEvaluator:
    """Test condition evaluation functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Enhanced workflow control modules not available")
        
        # Mock variables manager
        self.vars_manager = Mock()
        self.device_context = Mock()
        self.host_namespace = Mock()
        
        # Configure mocks
        self.device_context.get_flat_context.return_value = {
            "backup_enabled": True,
            "host_platform": "ios",
            "connectivity_result": {"success": True},
            "interface_count": 5
        }
        self.device_context.host_namespace = self.host_namespace
        self.host_namespace.platform = "ios"
        self.host_namespace.name = "router01"
        
        self.vars_manager.get_device_context.return_value = self.device_context
        
        self.evaluator = ConditionEvaluator(self.vars_manager, "router01")
    
    def test_simple_boolean_condition(self):
        """Test simple boolean condition evaluation."""
        result = self.evaluator.evaluate("{{ backup_enabled }}")
        assert result is True
        
        result = self.evaluator.evaluate("{{ not backup_enabled }}")
        assert result is False
    
    def test_comparison_condition(self):
        """Test comparison condition evaluation."""
        result = self.evaluator.evaluate("{{ host_platform == 'ios' }}")
        assert result is True
        
        result = self.evaluator.evaluate("{{ host_platform == 'junos' }}")
        assert result is False
    
    def test_complex_condition(self):
        """Test complex condition with multiple operators."""
        condition = "{{ backup_enabled and host_platform == 'ios' and connectivity_result.success }}"
        result = self.evaluator.evaluate(condition)
        assert result is True
    
    def test_numeric_condition(self):
        """Test numeric comparison conditions."""
        result = self.evaluator.evaluate("{{ interface_count > 3 }}")
        assert result is True
        
        result = self.evaluator.evaluate("{{ interface_count < 3 }}")
        assert result is False
    
    def test_list_membership_condition(self):
        """Test list membership conditions."""
        result = self.evaluator.evaluate("{{ host_platform in ['ios', 'nxos'] }}")
        assert result is True
        
        result = self.evaluator.evaluate("{{ host_platform in ['junos', 'eos'] }}")
        assert result is False
    
    def test_invalid_condition_handling(self):
        """Test handling of invalid conditions."""
        # Should return False for invalid conditions, not raise exception
        result = self.evaluator.evaluate("{{ invalid_variable }}")
        assert result is False


class TestRetryStrategy:
    """Test retry strategy functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Enhanced workflow control modules not available")
    
    def test_basic_retry_strategy(self):
        """Test basic retry strategy configuration."""
        strategy = RetryStrategy(max_attempts=3, delay=1.0)
        
        assert strategy.max_attempts == 3
        assert strategy.delay == 1.0
        assert strategy.backoff_factor == 2.0
        assert strategy.max_delay == 60.0
    
    def test_delay_calculation(self):
        """Test delay calculation with backoff."""
        strategy = RetryStrategy(max_attempts=5, delay=1.0, backoff_factor=2.0)
        
        # First attempt has no delay
        assert strategy.get_delay(1) == 0
        
        # Subsequent attempts have exponential backoff
        assert strategy.get_delay(2) == 1.0
        assert strategy.get_delay(3) == 2.0
        assert strategy.get_delay(4) == 4.0
        assert strategy.get_delay(5) == 8.0
    
    def test_max_delay_limit(self):
        """Test maximum delay limit."""
        strategy = RetryStrategy(delay=10.0, backoff_factor=3.0, max_delay=20.0)
        
        # Should not exceed max_delay
        delay = strategy.get_delay(5)  # Would be 10 * 3^3 = 270 without limit
        assert delay <= 20.0
    
    def test_should_retry_logic(self):
        """Test retry decision logic."""
        strategy = RetryStrategy(
            max_attempts=3,
            retry_on=["ConnectionError", "TimeoutError"]
        )
        
        # Should retry on specified exceptions
        connection_error = Exception("Connection failed")
        connection_error.__class__.__name__ = "ConnectionError"
        assert strategy.should_retry(connection_error, 1) is True
        assert strategy.should_retry(connection_error, 2) is True
        assert strategy.should_retry(connection_error, 3) is False  # Max attempts reached
        
        # Should not retry on other exceptions
        value_error = Exception("Invalid value")
        value_error.__class__.__name__ = "ValueError"
        assert strategy.should_retry(value_error, 1) is False


class TestLoopController:
    """Test loop controller functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Enhanced workflow control modules not available")
        
        # Mock variables manager
        self.vars_manager = Mock()
        self.device_context = Mock()
        
        self.device_context.get_flat_context.return_value = {
            "interface_list": ["GigE0/1", "GigE0/2", "GigE0/3"],
            "port_list": [22, 80, 443],
            "loop_condition": False
        }
        
        self.vars_manager.get_device_context.return_value = self.device_context
        
        self.controller = LoopController(self.vars_manager, "router01")
    
    def test_expand_simple_list(self):
        """Test expansion of simple list items."""
        items = ["item1", "item2", "item3"]
        result = self.controller.expand_items(items)
        assert result == items
    
    def test_expand_variable_reference(self):
        """Test expansion of variable reference."""
        result = self.controller.expand_items("{{ interface_list }}")
        assert result == ["GigE0/1", "GigE0/2", "GigE0/3"]
    
    def test_expand_single_item(self):
        """Test expansion of single item."""
        result = self.controller.expand_items("single_item")
        assert result == ["single_item"]
    
    def test_until_condition_evaluation(self):
        """Test until condition evaluation."""
        # Should continue when condition is False
        assert self.controller.should_continue_until("{{ loop_condition }}") is True
        
        # Should stop when condition is True
        self.device_context.get_flat_context.return_value["loop_condition"] = True
        assert self.controller.should_continue_until("{{ loop_condition }}") is False


class TestEnhancedTaskModel:
    """Test enhanced task model functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Enhanced workflow control modules not available")
        
        # Mock original task model
        self.task_model = Mock()
        self.task_model.name = "test_task"
        self.task_model.args = {"arg1": "value1"}
    
    def test_basic_task_model_creation(self):
        """Test basic enhanced task model creation."""
        enhanced_task = EnhancedTaskModel(self.task_model)
        
        assert enhanced_task.name == "test_task"
        assert enhanced_task.args == {"arg1": "value1"}
        assert enhanced_task.execution_mode == ExecutionMode.SEQUENTIAL
    
    def test_conditional_task_model(self):
        """Test conditional task model creation."""
        control_config = {"when": "{{ backup_enabled }}"}
        enhanced_task = EnhancedTaskModel(self.task_model, control_config)
        
        assert enhanced_task.when == "{{ backup_enabled }}"
        assert enhanced_task.execution_mode == ExecutionMode.CONDITIONAL
    
    def test_loop_task_model(self):
        """Test loop task model creation."""
        control_config = {"loop": ["item1", "item2", "item3"]}
        enhanced_task = EnhancedTaskModel(self.task_model, control_config)
        
        assert enhanced_task.loop == ["item1", "item2", "item3"]
        assert enhanced_task.execution_mode == ExecutionMode.LOOP
    
    def test_retry_task_model(self):
        """Test retry task model creation."""
        control_config = {"retry": {"max_attempts": 3, "delay": 2}}
        enhanced_task = EnhancedTaskModel(self.task_model, control_config)
        
        assert enhanced_task.retry == {"max_attempts": 3, "delay": 2}
        assert enhanced_task.execution_mode == ExecutionMode.RETRY
    
    def test_dependency_checking(self):
        """Test dependency checking functionality."""
        control_config = {"depends_on": ["task1", "task2"]}
        enhanced_task = EnhancedTaskModel(self.task_model, control_config)
        
        # Dependencies not met
        assert enhanced_task.check_dependencies(["task1"]) is False
        
        # All dependencies met
        assert enhanced_task.check_dependencies(["task1", "task2"]) is True
        assert enhanced_task.check_dependencies(["task1", "task2", "task3"]) is True
    
    def test_single_dependency_checking(self):
        """Test single dependency checking."""
        control_config = {"depends_on": "task1"}
        enhanced_task = EnhancedTaskModel(self.task_model, control_config)
        
        assert enhanced_task.check_dependencies([]) is False
        assert enhanced_task.check_dependencies(["task1"]) is True


class TestWorkflowParsing:
    """Test workflow parsing functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        if not IMPORTS_AVAILABLE:
            pytest.skip("Enhanced workflow control modules not available")
    
    def test_parse_basic_workflow(self):
        """Test parsing of basic workflow."""
        workflow_dict = {
            "workflow": {
                "name": "Test Workflow",
                "tasks": [
                    {
                        "name": "echo",
                        "args": {"msg": "Hello World"}
                    }
                ]
            }
        }
        
        with patch('enhancements.workflow_control.control_structures.TaskModel') as mock_task_model:
            mock_task_instance = Mock()
            mock_task_model.create.return_value = mock_task_instance
            
            enhanced_tasks = parse_enhanced_workflow(workflow_dict)
            
            assert len(enhanced_tasks) == 1
            assert isinstance(enhanced_tasks[0], EnhancedTaskModel)
    
    def test_parse_workflow_with_control_structures(self):
        """Test parsing of workflow with control structures."""
        workflow_dict = {
            "workflow": {
                "name": "Enhanced Test Workflow",
                "tasks": [
                    {
                        "name": "conditional_task",
                        "args": {"msg": "Conditional message"},
                        "when": "{{ condition_var }}",
                        "retry": {"max_attempts": 3}
                    },
                    {
                        "name": "loop_task",
                        "args": {"item": "{{ item }}"},
                        "loop": ["item1", "item2"],
                        "depends_on": "conditional_task"
                    }
                ]
            }
        }
        
        with patch('enhancements.workflow_control.control_structures.TaskModel') as mock_task_model:
            mock_task_model.create.return_value = Mock()
            
            enhanced_tasks = parse_enhanced_workflow(workflow_dict)
            
            assert len(enhanced_tasks) == 2
            
            # Check first task (conditional with retry)
            task1 = enhanced_tasks[0]
            assert task1.when == "{{ condition_var }}"
            assert task1.retry == {"max_attempts": 3}
            assert task1.execution_mode == ExecutionMode.CONDITIONAL
            
            # Check second task (loop with dependency)
            task2 = enhanced_tasks[1]
            assert task2.loop == ["item1", "item2"]
            assert task2.depends_on == "conditional_task"
            assert task2.execution_mode == ExecutionMode.LOOP


def run_integration_test():
    """Run a simple integration test."""
    if not IMPORTS_AVAILABLE:
        print("❌ Enhanced workflow control modules not available for integration test")
        return False
    
    print("🧪 Running Enhanced Workflow Control Integration Test")
    print("=" * 60)
    
    try:
        # Test condition evaluation
        print("✓ Testing condition evaluation...")
        vars_manager = Mock()
        device_context = Mock()
        device_context.get_flat_context.return_value = {"test_var": True}
        device_context.host_namespace = Mock()
        vars_manager.get_device_context.return_value = device_context
        
        evaluator = ConditionEvaluator(vars_manager, "test_host")
        result = evaluator.evaluate("{{ test_var }}")
        assert result is True
        
        # Test retry strategy
        print("✓ Testing retry strategy...")
        strategy = RetryStrategy(max_attempts=3, delay=1.0)
        assert strategy.get_delay(2) == 1.0
        
        # Test loop controller
        print("✓ Testing loop controller...")
        controller = LoopController(vars_manager, "test_host")
        items = controller.expand_items(["item1", "item2"])
        assert items == ["item1", "item2"]
        
        print("✅ Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print("🚀 Enhanced Workflow Control Test Suite")
    print("=" * 50)
    
    if not IMPORTS_AVAILABLE:
        print("❌ Cannot run tests - enhanced workflow control modules not available")
        print("   Make sure you're running from the correct directory")
        return
    
    # Run integration test
    success = run_integration_test()
    
    if success:
        print("\n📋 To run the full test suite with pytest:")
        print("   pytest test_enhanced_workflow_control.py -v")
        print("\n📋 To run specific test classes:")
        print("   pytest test_enhanced_workflow_control.py::TestConditionEvaluator -v")
        print("   pytest test_enhanced_workflow_control.py::TestRetryStrategy -v")
        print("   pytest test_enhanced_workflow_control.py::TestLoopController -v")
    else:
        print("\n❌ Integration test failed - check the error messages above")


if __name__ == "__main__":
    main()
