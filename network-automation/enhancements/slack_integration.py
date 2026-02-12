#!/usr/bin/env python3
"""
Slack Integration for AI Learning Loop.

Handles notifications about improvement sessions and results.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

import httpx

logger = logging.getLogger(__name__)


class SlackNotifier:
    """
    Manages Slack notifications for AI learning loop events.
    """
    
    def __init__(self, webhook_url: str, default_channel: str = "#automation"):
        """Initialize Slack notifier."""
        self.webhook_url = webhook_url
        self.default_channel = default_channel
        self.client = httpx.AsyncClient(timeout=30.0)
        
        logger.info(f"Slack notifier initialized for channel {default_channel}")
    
    async def send_notification(
        self,
        message: str,
        channel: str = None,
        attachments: List[Dict[str, Any]] = None,
        blocks: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send notification to Slack.
        
        Args:
            message: Main message text
            channel: Target channel (uses default if not specified)
            attachments: Slack message attachments
            blocks: Slack block kit elements
            
        Returns:
            Notification result
        """
        try:
            if not self.webhook_url:
                logger.warning("Slack webhook URL not configured, skipping notification")
                return {"success": False, "error": "Webhook URL not configured"}
            
            # Prepare payload
            payload = {
                "text": message,
                "channel": channel or self.default_channel,
                "username": "AI Learning Loop",
                "icon_emoji": ":robot_face:"
            }
            
            if attachments:
                payload["attachments"] = attachments
            
            if blocks:
                payload["blocks"] = blocks
            
            # Send to Slack
            response = await self.client.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                logger.info(f"Slack notification sent successfully to {channel or self.default_channel}")
                return {"success": True}
            else:
                logger.error(f"Slack notification failed: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def notify_improvement_start(
        self,
        workflow_name: str,
        user_requirements: str,
        device_types: List[str],
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify that improvement process has started."""
        message = f"🤖 **AI Learning Loop Started**\n\n**Workflow**: {workflow_name}\n**Devices**: {', '.join(device_types)}\n**Requirements**: {user_requirements[:200]}...\n\nStarting intelligent testing and improvement cycle! 🔄"
        
        attachments = [
            {
                "color": "good",
                "fields": [
                    {
                        "title": "Process",
                        "value": "Generate → Test → Analyze → Fix → Repeat until perfect",
                        "short": False
                    }
                ]
            }
        ]
        
        return await self.send_notification(message, channel, attachments)
    
    async def notify_improvement_success(
        self,
        session: Dict[str, Any],
        commit_url: str = None,
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify successful completion of improvement process."""
        attempts = len(session["attempts"])
        duration = session.get("duration_minutes", 0)
        
        message = f"✅ **AI Learning Loop SUCCESS!**\n\n**Workflow**: {session['workflow_name']}\n**Attempts**: {attempts}\n**Duration**: {duration:.1f} minutes\n**Status**: All tests passed! 🎉\n\nAutomation is production-ready and committed to GitHub! 🚀"
        
        attachments = [
            {
                "color": "good",
                "fields": [
                    {
                        "title": "Final Test Results",
                        "value": "✅ All connectivity tests passed\n✅ Workflow execution successful\n✅ Device validation complete",
                        "short": True
                    },
                    {
                        "title": "AI Improvements",
                        "value": f"Made {attempts} improvement iterations\nFixed all identified issues\nCode quality: Production ready",
                        "short": True
                    }
                ]
            }
        ]
        
        if commit_url:
            attachments[0]["fields"].append({
                "title": "GitHub Repository",
                "value": f"<{commit_url}|View Committed Code>",
                "short": False
            })
        
        return await self.send_notification(message, channel, attachments)
    
    async def notify_improvement_failure(
        self,
        session: Dict[str, Any],
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify failure of improvement process."""
        attempts = len(session["attempts"])
        
        # Get last failure analysis if available
        last_failure = "Unknown error"
        if session["attempts"]:
            last_attempt = session["attempts"][-1]
            if "failure_analysis" in last_attempt and last_attempt["failure_analysis"]:
                last_failure = last_attempt["failure_analysis"][0].get("root_cause", "Unknown error")
        
        message = f"❌ **AI Learning Loop Failed**\n\n**Workflow**: {session['workflow_name']}\n**Attempts**: {attempts}\n**Status**: Unable to fix all issues automatically\n\nManual review required 🔍"
        
        attachments = [
            {
                "color": "danger",
                "fields": [
                    {
                        "title": "Last Error Analysis",
                        "value": last_failure[:500] + ("..." if len(last_failure) > 500 else ""),
                        "short": False
                    },
                    {
                        "title": "Next Steps",
                        "value": "• Review session logs\n• Check device connectivity\n• Validate automation logic\n• Consider manual fixes",
                        "short": False
                    }
                ]
            }
        ]
        
        return await self.send_notification(message, channel, attachments)
    
    async def notify_improvement_progress(
        self,
        workflow_name: str,
        attempt: int,
        max_attempts: int,
        changes_made: List[str],
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify progress during improvement process."""
        message = f"🔄 **AI Learning Loop Progress**\n\n**Workflow**: {workflow_name}\n**Attempt**: {attempt}/{max_attempts}\n**Status**: Applying AI-generated fixes...\n\nContinuing improvement cycle! 🧠"
        
        attachments = [
            {
                "color": "warning",
                "fields": [
                    {
                        "title": "Changes Applied",
                        "value": "\n".join(f"• {change}" for change in changes_made[:5]),
                        "short": False
                    }
                ]
            }
        ]
        
        return await self.send_notification(message, channel, attachments)
    
    async def notify_environment_created(
        self,
        environment_id: str,
        device_types: List[str],
        environment_type: str,
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify that test environment has been created."""
        message = f"🧪 **Test Environment Ready**\n\n**Environment ID**: {environment_id}\n**Type**: {environment_type}\n**Devices**: {', '.join(device_types)}\n\nStarting automation testing! ⚡"
        
        return await self.send_notification(message, channel)
    
    async def notify_test_results(
        self,
        workflow_name: str,
        test_results: Dict[str, Any],
        passed: bool,
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify about test results."""
        status_emoji = "✅" if passed else "❌"
        status_text = "PASSED" if passed else "FAILED"
        
        message = f"{status_emoji} **Test Results: {status_text}**\n\n**Workflow**: {workflow_name}\n**Status**: {status_text}\n\n"
        
        if passed:
            message += "All tests completed successfully! Ready for production deployment! 🚀"
            color = "good"
        else:
            message += "Tests failed. AI is analyzing failures and generating fixes... 🔧"
            color = "warning"
        
        # Extract test summary
        test_summary = []
        if "detailed_results" in test_results:
            for test_name, result in test_results["detailed_results"].items():
                status = "✅" if result.get("status") == "passed" else "❌"
                test_summary.append(f"{status} {test_name}")
        
        attachments = [
            {
                "color": color,
                "fields": [
                    {
                        "title": "Test Summary",
                        "value": "\n".join(test_summary) if test_summary else "No detailed results available",
                        "short": False
                    }
                ]
            }
        ]
        
        return await self.send_notification(message, channel, attachments)
    
    async def notify_error(
        self,
        error_message: str,
        context: str = None,
        channel: str = None
    ) -> Dict[str, Any]:
        """Notify about system errors."""
        message = f"⚠️ **AI Learning Loop Error**\n\n**Error**: {error_message}\n\n"
        
        if context:
            message += f"**Context**: {context}\n\n"
        
        message += "System administrators have been notified. 🛠️"
        
        attachments = [
            {
                "color": "danger",
                "fields": [
                    {
                        "title": "Action Required",
                        "value": "Check system logs and restart services if necessary",
                        "short": False
                    }
                ]
            }
        ]
        
        return await self.send_notification(message, channel, attachments)
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
