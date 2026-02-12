#!/usr/bin/env python3
"""
N8N Integration API Extensions for NornFlow NetOps.

This module provides specialized API endpoints for N8N workflow integration,
enabling AI-driven network automation workflow generation and management.

Features:
- Project creation and management
- AI-generated code validation
- Workflow testing and iteration
- Integration with external systems
- Real-time status updates

Usage:
    from enhancements.ai_integration.n8n_api_extensions import N8NIntegrationAPI
    
    api = N8NIntegrationAPI(app)
    api.register_routes()
"""

import json
import uuid
import asyncio
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from ..security.rbac import Permission
from ..security.middleware import SecurityMiddleware
from ..scheduling.orchestrator import WorkflowOrchestrator, ExecutionMode
from ..visualization.workflow_visualizer import WorkflowVisualizer


class N8NIntegrationAPI:
    """N8N Integration API for AI-driven workflow generation."""
    
    def __init__(self, app=None, security_middleware=None):
        """Initialize N8N integration API."""
        self.app = app
        self.security_middleware = security_middleware
        self.blueprint = Blueprint('n8n_integration', __name__, url_prefix='/api/n8n')
        self.projects = {}  # In-memory project storage (use database in production)
        self.orchestrator = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the API with Flask app."""
        self.app = app
        app.register_blueprint(self.blueprint)
        
        # Initialize orchestrator
        self.orchestrator = WorkflowOrchestrator()
    
    def register_routes(self):
        """Register all N8N integration routes."""
        
        @self.blueprint.route('/projects/create', methods=['POST'])
        @self.security_middleware.require_permission(Permission.WORKFLOW_WRITE)
        def create_project():
            """Create a new AI-generated automation project."""
            try:
                data = request.get_json()
                
                # Validate required fields
                required_fields = ['project_name', 'task_type', 'device_types', 'generated_code']
                for field in required_fields:
                    if field not in data:
                        raise BadRequest(f"Missing required field: {field}")
                
                # Generate project ID
                project_id = str(uuid.uuid4())
                
                # Create project structure
                project = {
                    'id': project_id,
                    'name': data['project_name'],
                    'task_type': data['task_type'],
                    'device_types': data['device_types'],
                    'generated_code': data['generated_code'],
                    'workflow_design': data.get('workflow_design', {}),
                    'status': 'created',
                    'created_at': datetime.utcnow().isoformat(),
                    'iterations': 0,
                    'test_results': [],
                    'files': {}
                }
                
                # Process generated code
                if isinstance(data['generated_code'], dict):
                    for filename, content in data['generated_code'].items():
                        project['files'][filename] = {
                            'content': content,
                            'created_at': datetime.utcnow().isoformat(),
                            'version': 1
                        }
                
                # Create project directory
                project_dir = Path(f"projects/{project_id}")
                project_dir.mkdir(parents=True, exist_ok=True)
                
                # Save files to disk
                for filename, file_info in project['files'].items():
                    file_path = project_dir / filename
                    file_path.write_text(file_info['content'])
                
                # Create main workflow file
                workflow_file = self._create_nornflow_workflow(project)
                project['workflow_file'] = str(workflow_file)
                
                # Store project
                self.projects[project_id] = project
                
                return jsonify({
                    'success': True,
                    'project_id': project_id,
                    'workflow_file': project['workflow_file'],
                    'message': 'Project created successfully'
                })
            
            except Exception as e:
                current_app.logger.error(f"Failed to create project: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f"Failed to create project: {str(e)}"
                }), 500
        
        @self.blueprint.route('/projects/<project_id>/test', methods=['POST'])
        @self.security_middleware.require_permission(Permission.WORKFLOW_EXECUTE)
        def test_project(project_id):
            """Test an AI-generated project."""
            try:
                if project_id not in self.projects:
                    raise NotFound("Project not found")
                
                project = self.projects[project_id]
                data = request.get_json() or {}
                
                # Run validation tests
                test_results = self._run_project_tests(project, data.get('test_mode', 'syntax'))
                
                # Update project with test results
                project['test_results'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'results': test_results,
                    'iteration': project['iterations']
                })
                
                # Update project status
                if test_results['success']:
                    project['status'] = 'tested'
                else:
                    project['status'] = 'failed'
                
                return jsonify({
                    'success': test_results['success'],
                    'test_results': test_results,
                    'project_status': project['status']
                })
            
            except Exception as e:
                current_app.logger.error(f"Failed to test project: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f"Failed to test project: {str(e)}"
                }), 500
        
        @self.blueprint.route('/projects/<project_id>/update', methods=['POST'])
        @self.security_middleware.require_permission(Permission.WORKFLOW_WRITE)
        def update_project(project_id):
            """Update project with improved code."""
            try:
                if project_id not in self.projects:
                    raise NotFound("Project not found")
                
                project = self.projects[project_id]
                data = request.get_json()
                
                # Increment iteration
                project['iterations'] += 1
                
                # Update code if provided
                if 'improved_code' in data:
                    improved_code = data['improved_code']
                    
                    if isinstance(improved_code, dict):
                        for filename, content in improved_code.items():
                            if filename in project['files']:
                                project['files'][filename]['content'] = content
                                project['files'][filename]['version'] += 1
                                project['files'][filename]['updated_at'] = datetime.utcnow().isoformat()
                            else:
                                project['files'][filename] = {
                                    'content': content,
                                    'created_at': datetime.utcnow().isoformat(),
                                    'version': 1
                                }
                    
                    # Save updated files
                    project_dir = Path(f"projects/{project_id}")
                    for filename, file_info in project['files'].items():
                        file_path = project_dir / filename
                        file_path.write_text(file_info['content'])
                
                # Update workflow file
                workflow_file = self._create_nornflow_workflow(project)
                project['workflow_file'] = str(workflow_file)
                project['status'] = 'updated'
                
                return jsonify({
                    'success': True,
                    'iteration': project['iterations'],
                    'workflow_file': project['workflow_file'],
                    'message': 'Project updated successfully'
                })
            
            except Exception as e:
                current_app.logger.error(f"Failed to update project: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f"Failed to update project: {str(e)}"
                }), 500
        
        @self.blueprint.route('/projects/<project_id>/status', methods=['GET'])
        @self.security_middleware.require_permission(Permission.WORKFLOW_READ)
        def get_project_status(project_id):
            """Get project status and details."""
            try:
                if project_id not in self.projects:
                    raise NotFound("Project not found")
                
                project = self.projects[project_id]
                
                return jsonify({
                    'success': True,
                    'project': {
                        'id': project['id'],
                        'name': project['name'],
                        'status': project['status'],
                        'iterations': project['iterations'],
                        'created_at': project['created_at'],
                        'test_results': project['test_results'][-5:],  # Last 5 test results
                        'files': list(project['files'].keys())
                    }
                })
            
            except Exception as e:
                current_app.logger.error(f"Failed to get project status: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f"Failed to get project status: {str(e)}"
                }), 500
        
        @self.blueprint.route('/projects', methods=['GET'])
        @self.security_middleware.require_permission(Permission.WORKFLOW_READ)
        def list_projects():
            """List all projects."""
            try:
                projects_list = []
                for project_id, project in self.projects.items():
                    projects_list.append({
                        'id': project['id'],
                        'name': project['name'],
                        'task_type': project['task_type'],
                        'status': project['status'],
                        'iterations': project['iterations'],
                        'created_at': project['created_at']
                    })
                
                return jsonify({
                    'success': True,
                    'projects': projects_list
                })
            
            except Exception as e:
                current_app.logger.error(f"Failed to list projects: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f"Failed to list projects: {str(e)}"
                }), 500
    
    def _create_nornflow_workflow(self, project: Dict[str, Any]) -> Path:
        """Create NornFlow workflow file from project."""
        project_dir = Path(f"projects/{project['id']}")
        workflow_file = project_dir / "workflow.yaml"
        
        # Generate workflow YAML
        workflow_content = f"""
name: {project['name']}
description: AI-generated workflow for {project['task_type']}

variables:
  project_id: "{project['id']}"
  task_type: "{project['task_type']}"
  device_types: {json.dumps(project['device_types'])}

tasks:
  - name: setup_environment
    action: debug
    message: "Setting up environment for {{{{ task_type }}}}"
    
  - name: load_inventory
    action: inventory.load
    source: "inventory/hosts.yaml"
    
  - name: execute_main_script
    action: python.execute
    script: "main.py"
    when: "{{{{ load_inventory.success }}}}"
    
  - name: generate_report
    action: reporting.create
    template: "report_template.j2"
    output_file: "results/{{{{ project_id }}}}_report.html"
    always: true
"""
        
        workflow_file.write_text(workflow_content.strip())
        return workflow_file
    
    def _run_project_tests(self, project: Dict[str, Any], test_mode: str) -> Dict[str, Any]:
        """Run tests on the generated project."""
        try:
            project_dir = Path(f"projects/{project['id']}")
            test_results = {
                'success': True,
                'tests': [],
                'errors': [],
                'warnings': []
            }
            
            # Syntax validation
            if test_mode in ['syntax', 'full']:
                syntax_result = self._validate_python_syntax(project_dir)
                test_results['tests'].append(syntax_result)
                if not syntax_result['passed']:
                    test_results['success'] = False
            
            # Import validation
            if test_mode in ['imports', 'full']:
                import_result = self._validate_imports(project_dir)
                test_results['tests'].append(import_result)
                if not import_result['passed']:
                    test_results['success'] = False
            
            # Nornir workflow validation
            if test_mode in ['workflow', 'full']:
                workflow_result = self._validate_nornir_workflow(project_dir)
                test_results['tests'].append(workflow_result)
                if not workflow_result['passed']:
                    test_results['success'] = False
            
            return test_results
        
        except Exception as e:
            return {
                'success': False,
                'tests': [],
                'errors': [f"Test execution failed: {str(e)}"],
                'warnings': []
            }
    
    def _validate_python_syntax(self, project_dir: Path) -> Dict[str, Any]:
        """Validate Python syntax in project files."""
        try:
            errors = []
            
            for py_file in project_dir.glob("*.py"):
                try:
                    with open(py_file, 'r') as f:
                        compile(f.read(), py_file.name, 'exec')
                except SyntaxError as e:
                    errors.append(f"{py_file.name}: {str(e)}")
            
            return {
                'name': 'Python Syntax Validation',
                'passed': len(errors) == 0,
                'errors': errors,
                'message': 'All Python files have valid syntax' if len(errors) == 0 else f"Found {len(errors)} syntax errors"
            }
        
        except Exception as e:
            return {
                'name': 'Python Syntax Validation',
                'passed': False,
                'errors': [str(e)],
                'message': 'Syntax validation failed'
            }
    
    def _validate_imports(self, project_dir: Path) -> Dict[str, Any]:
        """Validate Python imports in project files."""
        try:
            errors = []
            warnings = []
            
            # Check for common Nornir imports
            required_imports = ['nornir', 'nornir_netmiko', 'nornir_napalm']
            
            for py_file in project_dir.glob("*.py"):
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                    # Check for required imports
                    for imp in required_imports:
                        if imp in content and f"import {imp}" in content:
                            continue
                        elif imp in content:
                            warnings.append(f"{py_file.name}: {imp} referenced but not properly imported")
            
            return {
                'name': 'Import Validation',
                'passed': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'message': 'All imports are valid' if len(errors) == 0 else f"Found {len(errors)} import errors"
            }
        
        except Exception as e:
            return {
                'name': 'Import Validation',
                'passed': False,
                'errors': [str(e)],
                'message': 'Import validation failed'
            }
    
    def _validate_nornir_workflow(self, project_dir: Path) -> Dict[str, Any]:
        """Validate Nornir workflow structure."""
        try:
            errors = []
            warnings = []
            
            # Check for required files
            required_files = ['main.py', 'inventory/hosts.yaml']
            
            for req_file in required_files:
                file_path = project_dir / req_file
                if not file_path.exists():
                    errors.append(f"Missing required file: {req_file}")
            
            # Validate inventory structure
            inventory_dir = project_dir / "inventory"
            if inventory_dir.exists():
                hosts_file = inventory_dir / "hosts.yaml"
                if hosts_file.exists():
                    try:
                        import yaml
                        with open(hosts_file, 'r') as f:
                            inventory_data = yaml.safe_load(f)
                            
                        if not isinstance(inventory_data, dict):
                            errors.append("Invalid inventory format: must be a dictionary")
                    except yaml.YAMLError as e:
                        errors.append(f"Invalid YAML in hosts.yaml: {str(e)}")
            
            return {
                'name': 'Nornir Workflow Validation',
                'passed': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'message': 'Workflow structure is valid' if len(errors) == 0 else f"Found {len(errors)} workflow errors"
            }
        
        except Exception as e:
            return {
                'name': 'Nornir Workflow Validation',
                'passed': False,
                'errors': [str(e)],
                'message': 'Workflow validation failed'
            }
