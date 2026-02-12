#!/usr/bin/env python3
"""
Iterative Improvement Engine for Network Automation.

This module implements the intelligent learning loop that automatically
fixes failed network automation until tests pass, then commits to GitHub.
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
import tempfile
import shutil

from .failure_analyzer import ClaudeFailureAnalyzer, FailureAnalysisManager
from ..github_integration import GitHubManager
from ..slack_integration import SlackNotifier

logger = logging.getLogger(__name__)


class IterativeImprovementEngine:
    """
    Intelligent learning loop that automatically fixes network automation failures.
    
    Workflow:
    1. Test generated automation in LabFlow environment
    2. If test fails, analyze failure with Claude AI
    3. Generate and apply fixes to the code
    4. Re-test with updated code
    5. Repeat until tests pass or max attempts reached
    6. Commit successful automation to GitHub
    7. Notify team via Slack
    """
    
    def __init__(
        self,
        claude_api_key: str,
        github_manager: GitHubManager,
        slack_notifier: SlackNotifier,
        max_improvement_attempts: int = 5,
        min_confidence_threshold: float = 0.7
    ):
        """Initialize iterative improvement engine."""
        self.claude_analyzer = ClaudeFailureAnalyzer(claude_api_key)
        self.failure_manager = FailureAnalysisManager(self.claude_analyzer)
        self.github_manager = github_manager
        self.slack_notifier = slack_notifier
        self.max_attempts = max_improvement_attempts
        self.min_confidence = min_confidence_threshold
        
        # Track improvement sessions
        self.improvement_sessions: List[Dict[str, Any]] = []
        
        logger.info("Iterative improvement engine initialized")
    
    async def improve_until_success(
        self,
        workflow_name: str,
        initial_code: Dict[str, str],
        labflow_manager,
        environment_config: Dict[str, Any],
        user_requirements: str,
        project_id: str = None
    ) -> Dict[str, Any]:
        """
        Main improvement loop - keeps fixing code until tests pass.
        
        Args:
            workflow_name: Name of the workflow being improved
            initial_code: Initial generated code to test and improve
            labflow_manager: LabFlow manager for environment creation and testing
            environment_config: Environment configuration for testing
            user_requirements: Original user requirements for context
            project_id: Project ID for tracking
            
        Returns:
            Improvement session results with final code and status
        """
        session_id = f"improve_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            "session_id": session_id,
            "workflow_name": workflow_name,
            "start_time": datetime.utcnow().isoformat(),
            "user_requirements": user_requirements,
            "project_id": project_id,
            "attempts": [],
            "final_status": "in_progress",
            "final_code": None,
            "environment_id": None
        }
        
        try:
            logger.info(f"Starting improvement session {session_id} for workflow '{workflow_name}'")
            
            # Notify start of improvement process
            await self._notify_improvement_start(workflow_name, user_requirements)
            
            # Create test environment
            environment_result = await self._create_test_environment(
                labflow_manager, environment_config, session_id
            )
            
            if not environment_result["success"]:
                session["final_status"] = "environment_failed"
                session["error"] = environment_result["message"]
                return session
            
            session["environment_id"] = environment_result["environment_id"]
            
            # Start improvement loop
            current_code = initial_code.copy()
            
            for attempt in range(1, self.max_attempts + 1):
                logger.info(f"Improvement attempt {attempt}/{self.max_attempts}")
                
                attempt_result = await self._execute_improvement_attempt(
                    attempt=attempt,
                    current_code=current_code,
                    labflow_manager=labflow_manager,
                    environment_id=session["environment_id"],
                    workflow_name=workflow_name,
                    user_requirements=user_requirements
                )
                
                session["attempts"].append(attempt_result)
                
                if attempt_result["test_passed"]:
                    # Success! Tests passed
                    session["final_status"] = "success"
                    session["final_code"] = current_code
                    
                    # Commit to GitHub
                    commit_result = await self._commit_successful_automation(
                        workflow_name, current_code, session, user_requirements
                    )
                    session["commit_result"] = commit_result
                    
                    # Notify success
                    await self._notify_improvement_success(session)
                    
                    logger.info(f"Improvement session {session_id} completed successfully after {attempt} attempts")
                    break
                
                elif attempt_result["should_retry"] and attempt < self.max_attempts:
                    # Apply fixes and continue
                    current_code = attempt_result["updated_code"]
                    logger.info(f"Applying fixes and retrying (attempt {attempt + 1})")
                    
                    # Brief pause between attempts
                    await asyncio.sleep(5)
                
                else:
                    # No more retries or fixes not recommended
                    session["final_status"] = "failed"
                    session["final_code"] = current_code
                    
                    await self._notify_improvement_failure(session)
                    
                    logger.warning(f"Improvement session {session_id} failed after {attempt} attempts")
                    break
            
            # Cleanup environment
            await self._cleanup_test_environment(labflow_manager, session["environment_id"])
            
        except Exception as e:
            logger.error(f"Improvement session {session_id} encountered error: {str(e)}")
            session["final_status"] = "error"
            session["error"] = str(e)
            
            await self._notify_improvement_error(session, str(e))
        
        finally:
            session["end_time"] = datetime.utcnow().isoformat()
            session["duration_minutes"] = self._calculate_duration(session)
            self.improvement_sessions.append(session)
        
        return session
    
    async def _execute_improvement_attempt(
        self,
        attempt: int,
        current_code: Dict[str, str],
        labflow_manager,
        environment_id: str,
        workflow_name: str,
        user_requirements: str
    ) -> Dict[str, Any]:
        """Execute a single improvement attempt."""
        attempt_start = datetime.utcnow()
        
        attempt_result = {
            "attempt": attempt,
            "start_time": attempt_start.isoformat(),
            "test_passed": False,
            "should_retry": False,
            "updated_code": current_code.copy(),
            "test_results": None,
            "failure_analysis": None,
            "changes_applied": []
        }
        
        try:
            # Test current code
            logger.info(f"Testing code (attempt {attempt})")
            test_response = await labflow_manager.test_workflow(
                environment_id=environment_id,
                workflow_code=current_code,
                test_scenarios=None  # Auto-generate test scenarios
            )

            # Extract test results from LabFlow response
            if not test_response.get("success"):
                raise Exception(f"LabFlow testing failed: {test_response.get('message')}")

            test_results = test_response.get("results", {})
            attempt_result["test_results"] = test_results

            if test_results.get("overall_status") == "passed":
                # Tests passed!
                attempt_result["test_passed"] = True
                logger.info(f"Tests passed on attempt {attempt}!")
                return attempt_result
            
            # Tests failed - analyze and fix
            logger.info(f"Tests failed on attempt {attempt}, analyzing failure...")
            
            # Get environment info for analysis context
            environment_info = await labflow_manager.get_environment_status(environment_id)
            
            # Analyze failure and get fixes
            should_retry, updated_code, analyses = await self.failure_manager.analyze_and_suggest_fixes(
                test_results=test_results,
                workflow_code=current_code,
                environment_info=environment_info,
                max_attempts=1  # Single analysis per improvement attempt
            )
            
            attempt_result["should_retry"] = should_retry
            attempt_result["updated_code"] = updated_code
            attempt_result["failure_analysis"] = [
                {
                    "failure_type": analysis.failure_type,
                    "root_cause": analysis.root_cause,
                    "suggested_fixes": analysis.suggested_fixes,
                    "confidence_score": analysis.confidence_score
                }
                for analysis in analyses
            ]
            
            # Track what changes were applied
            if should_retry:
                changes = []
                for filename in updated_code:
                    if filename in current_code and updated_code[filename] != current_code[filename]:
                        changes.append(f"Modified {filename}")
                    elif filename not in current_code:
                        changes.append(f"Added {filename}")
                
                attempt_result["changes_applied"] = changes
                logger.info(f"Applied {len(changes)} code changes based on AI analysis")
            
        except Exception as e:
            logger.error(f"Improvement attempt {attempt} failed: {str(e)}")
            attempt_result["error"] = str(e)
        
        finally:
            attempt_result["end_time"] = datetime.utcnow().isoformat()
            attempt_result["duration_seconds"] = (
                datetime.utcnow() - attempt_start
            ).total_seconds()
        
        return attempt_result
    
    async def _create_test_environment(
        self,
        labflow_manager,
        environment_config: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Create test environment for improvement session."""
        try:
            environment_name = f"improve-{session_id}"
            
            result = await labflow_manager.create_environment(
                name=environment_name,
                environment_type=environment_config.get("environment_type", "auto"),
                device_types=environment_config.get("device_types", ["Linux"]),
                topology_requirements=environment_config.get("topology_requirements", {}),
                duration_hours=2,  # Short duration for improvement testing
                project_id=session_id
            )
            
            if result["success"]:
                # Wait for environment to be ready
                environment_id = result["environment_id"]
                await self._wait_for_environment_ready(labflow_manager, environment_id)
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to create test environment: {str(e)}")
            return {"success": False, "message": str(e)}
    
    async def _wait_for_environment_ready(
        self,
        labflow_manager,
        environment_id: str,
        max_wait_minutes: int = 10
    ):
        """Wait for environment to be ready for testing."""
        for _ in range(max_wait_minutes * 6):  # Check every 10 seconds
            status = await labflow_manager.get_environment_status(environment_id)
            if status.get("status") == "ready":
                logger.info(f"Environment {environment_id} is ready")
                return
            elif status.get("status") == "error":
                raise Exception(f"Environment {environment_id} failed to start")
            
            await asyncio.sleep(10)
        
        raise Exception(f"Environment {environment_id} not ready after {max_wait_minutes} minutes")
    
    async def _commit_successful_automation(
        self,
        workflow_name: str,
        final_code: Dict[str, str],
        session: Dict[str, Any],
        user_requirements: str
    ) -> Dict[str, Any]:
        """Commit successful automation to GitHub."""
        try:
            # Create commit message with improvement details
            attempts_count = len(session["attempts"])
            commit_message = f"""🤖 AI-Improved Network Automation: {workflow_name}

✅ AUTOMATED IMPROVEMENT COMPLETE:
- Original Requirements: {user_requirements[:100]}...
- Improvement Attempts: {attempts_count}
- Final Status: Success after iterative AI fixes
- Session ID: {session["session_id"]}

🧠 AI LEARNING LOOP RESULTS:
- Tests Passed: ✅ All validation successful
- Code Quality: Enhanced through AI analysis
- Device Compatibility: Verified in lab environment
- Ready for Production: ✅

Generated and improved by AI-powered automation pipeline.
"""
            
            # Prepare files for commit
            files_to_commit = {}
            for filename, content in final_code.items():
                # Organize files in workflow directory
                file_path = f"workflows/{workflow_name}/{filename}"
                files_to_commit[file_path] = content
            
            # Add session metadata
            session_metadata = {
                "session_id": session["session_id"],
                "workflow_name": workflow_name,
                "user_requirements": user_requirements,
                "improvement_summary": {
                    "total_attempts": len(session["attempts"]),
                    "final_status": session["final_status"],
                    "duration_minutes": session.get("duration_minutes", 0)
                },
                "test_results": session["attempts"][-1]["test_results"] if session["attempts"] else None
            }
            
            files_to_commit[f"workflows/{workflow_name}/improvement_session.json"] = json.dumps(
                session_metadata, indent=2
            )
            
            # Commit to GitHub
            commit_result = await self.github_manager.commit_files(
                files=files_to_commit,
                commit_message=commit_message,
                branch=f"ai-improved-{workflow_name}"
            )
            
            logger.info(f"Successfully committed improved automation to GitHub: {commit_result}")
            return commit_result
        
        except Exception as e:
            logger.error(f"Failed to commit successful automation: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _cleanup_test_environment(self, labflow_manager, environment_id: str):
        """Clean up test environment after improvement session."""
        try:
            if environment_id:
                await labflow_manager.destroy_environment(environment_id)
                logger.info(f"Cleaned up test environment {environment_id}")
        except Exception as e:
            logger.warning(f"Failed to cleanup environment {environment_id}: {str(e)}")
    
    async def _notify_improvement_start(self, workflow_name: str, user_requirements: str):
        """Notify team that improvement process has started."""
        message = f"""🤖 **AI Improvement Started**

**Workflow**: {workflow_name}
**Requirements**: {user_requirements[:200]}...

Starting intelligent learning loop to test and improve automation until perfect! 🔄"""
        
        await self.slack_notifier.send_notification(message, channel="automation")
    
    async def _notify_improvement_success(self, session: Dict[str, Any]):
        """Notify team of successful improvement."""
        attempts = len(session["attempts"])
        duration = session.get("duration_minutes", 0)
        
        message = f"""✅ **AI Improvement SUCCESS!**

**Workflow**: {session["workflow_name"]}
**Attempts**: {attempts}
**Duration**: {duration:.1f} minutes
**Status**: Tests passing, committed to GitHub! 🚀

The AI learning loop successfully fixed all issues and delivered working automation! 🎯"""
        
        await self.slack_notifier.send_notification(message, channel="automation")
    
    async def _notify_improvement_failure(self, session: Dict[str, Any]):
        """Notify team of improvement failure."""
        attempts = len(session["attempts"])
        
        message = f"""❌ **AI Improvement Failed**

**Workflow**: {session["workflow_name"]}
**Attempts**: {attempts}/{self.max_attempts}
**Status**: Unable to fix all issues automatically

Manual review required. Check improvement session details for analysis. 🔍"""
        
        await self.slack_notifier.send_notification(message, channel="automation")
    
    async def _notify_improvement_error(self, session: Dict[str, Any], error: str):
        """Notify team of improvement error."""
        message = f"""⚠️ **AI Improvement Error**

**Workflow**: {session["workflow_name"]}
**Error**: {error}

Improvement process encountered an unexpected error. Manual intervention required. 🛠️"""
        
        await self.slack_notifier.send_notification(message, channel="automation")
    
    def _calculate_duration(self, session: Dict[str, Any]) -> float:
        """Calculate session duration in minutes."""
        if "start_time" in session and "end_time" in session:
            start = datetime.fromisoformat(session["start_time"])
            end = datetime.fromisoformat(session["end_time"])
            return (end - start).total_seconds() / 60
        return 0.0
    
    def get_improvement_statistics(self) -> Dict[str, Any]:
        """Get statistics about improvement sessions."""
        if not self.improvement_sessions:
            return {"total_sessions": 0}
        
        successful_sessions = [s for s in self.improvement_sessions if s["final_status"] == "success"]
        
        return {
            "total_sessions": len(self.improvement_sessions),
            "successful_sessions": len(successful_sessions),
            "success_rate": len(successful_sessions) / len(self.improvement_sessions),
            "average_attempts": sum(len(s["attempts"]) for s in self.improvement_sessions) / len(self.improvement_sessions),
            "average_duration_minutes": sum(s.get("duration_minutes", 0) for s in self.improvement_sessions) / len(self.improvement_sessions),
            "common_failure_types": self.failure_manager._get_common_failure_types()
        }
    
    async def close(self):
        """Close the improvement engine and cleanup resources."""
        await self.claude_analyzer.close()
        logger.info("Iterative improvement engine closed")
