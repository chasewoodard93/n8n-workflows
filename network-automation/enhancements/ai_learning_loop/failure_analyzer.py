#!/usr/bin/env python3
"""
AI Failure Analyzer for LabFlow.

This module provides intelligent failure analysis using Claude AI to analyze
test failures and automatically generate fixes for network automation code.
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

import httpx
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FailureAnalysis:
    """Represents an AI analysis of a test failure."""
    failure_type: str
    root_cause: str
    suggested_fixes: List[str]
    code_changes: Dict[str, str]
    confidence_score: float
    retry_recommended: bool


class ClaudeFailureAnalyzer:
    """
    AI-powered failure analyzer using Claude API.
    
    Analyzes test failures and generates intelligent fixes for network automation code.
    """
    
    def __init__(self, api_key: str, api_url: str = "https://api.anthropic.com/v1/messages"):
        """Initialize Claude failure analyzer."""
        self.api_key = api_key
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=60.0)
        
        # Failure pattern database for quick classification
        self.failure_patterns = {
            "connection_timeout": {
                "patterns": [r"timeout", r"connection.*failed", r"unreachable"],
                "category": "connectivity"
            },
            "authentication_failed": {
                "patterns": [r"authentication.*failed", r"invalid.*credentials", r"permission.*denied"],
                "category": "authentication"
            },
            "syntax_error": {
                "patterns": [r"syntax.*error", r"invalid.*syntax", r"unexpected.*token"],
                "category": "code_syntax"
            },
            "import_error": {
                "patterns": [r"import.*error", r"module.*not.*found", r"no.*module.*named"],
                "category": "dependencies"
            },
            "configuration_error": {
                "patterns": [r"configuration.*error", r"invalid.*config", r"command.*not.*found"],
                "category": "device_config"
            }
        }
        
        logger.info("Claude failure analyzer initialized")
    
    async def analyze_failure(
        self,
        test_results: Dict[str, Any],
        workflow_code: Dict[str, str],
        environment_info: Dict[str, Any],
        previous_attempts: List[Dict[str, Any]] = None
    ) -> FailureAnalysis:
        """
        Analyze test failure and generate intelligent fixes.
        
        Args:
            test_results: Failed test results with error details
            workflow_code: Current workflow code that failed
            environment_info: Information about test environment
            previous_attempts: Previous fix attempts to avoid repeating
            
        Returns:
            FailureAnalysis with suggested fixes
        """
        try:
            logger.info("Starting AI failure analysis")
            
            # Quick pattern-based classification
            failure_type = self._classify_failure(test_results)
            
            # Prepare context for Claude
            analysis_context = self._prepare_analysis_context(
                test_results, workflow_code, environment_info, previous_attempts
            )
            
            # Get AI analysis from Claude
            claude_response = await self._query_claude_for_analysis(analysis_context)
            
            # Parse Claude response into structured analysis
            analysis = self._parse_claude_response(claude_response, failure_type)
            
            logger.info(f"Failure analysis completed: {analysis.failure_type} (confidence: {analysis.confidence_score})")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Failure analysis failed: {str(e)}")
            # Return fallback analysis
            return FailureAnalysis(
                failure_type="unknown",
                root_cause=f"Analysis failed: {str(e)}",
                suggested_fixes=["Manual review required"],
                code_changes={},
                confidence_score=0.1,
                retry_recommended=False
            )
    
    def _classify_failure(self, test_results: Dict[str, Any]) -> str:
        """Quickly classify failure type using pattern matching."""
        error_text = ""
        
        # Extract error messages from test results
        if "detailed_results" in test_results:
            for test_name, result in test_results["detailed_results"].items():
                if result.get("status") == "failed":
                    error_text += f" {result.get('details', '')} {result.get('error_message', '')}"
        
        error_text = error_text.lower()
        
        # Check patterns
        for failure_type, config in self.failure_patterns.items():
            for pattern in config["patterns"]:
                if re.search(pattern, error_text):
                    return failure_type
        
        return "unknown"
    
    def _prepare_analysis_context(
        self,
        test_results: Dict[str, Any],
        workflow_code: Dict[str, str],
        environment_info: Dict[str, Any],
        previous_attempts: List[Dict[str, Any]]
    ) -> str:
        """Prepare comprehensive context for Claude analysis."""
        
        context = f"""
# Network Automation Failure Analysis Request

## Test Environment
- Environment Type: {environment_info.get('environment_type', 'unknown')}
- Device Types: {', '.join(environment_info.get('device_types', []))}
- Management IPs: {json.dumps(environment_info.get('management_ips', {}), indent=2)}
- Access Info: {json.dumps(environment_info.get('access_info', {}), indent=2)}

## Failed Test Results
```json
{json.dumps(test_results, indent=2)}
```

## Current Workflow Code
"""
        
        # Add all workflow files
        for filename, code in workflow_code.items():
            context += f"\n### {filename}\n```python\n{code}\n```\n"
        
        # Add previous attempts if any
        if previous_attempts:
            context += "\n## Previous Fix Attempts\n"
            for i, attempt in enumerate(previous_attempts, 1):
                context += f"\n### Attempt {i}\n"
                context += f"- Changes Made: {attempt.get('changes_description', 'Unknown')}\n"
                context += f"- Result: {attempt.get('result', 'Failed')}\n"
                context += f"- Error: {attempt.get('error', 'Unknown')}\n"
        
        context += """

## Analysis Request
Please analyze this network automation failure and provide:

1. **Root Cause Analysis**: What exactly went wrong and why?
2. **Failure Classification**: Type of failure (connectivity, authentication, syntax, configuration, etc.)
3. **Specific Fixes**: Concrete code changes needed to fix the issue
4. **Code Modifications**: Exact file modifications with before/after code
5. **Confidence Assessment**: How confident you are this fix will work (0.0-1.0)
6. **Retry Recommendation**: Whether this fix should be automatically retried

Focus on:
- Network device connectivity and authentication issues
- Nornir framework specific problems
- Device configuration syntax errors
- Inventory and credential management
- Common network automation pitfalls

Provide response in this JSON format:
{
  "root_cause": "Detailed explanation of what went wrong",
  "failure_type": "connectivity|authentication|syntax|configuration|dependencies|unknown",
  "suggested_fixes": ["List of specific fixes to implement"],
  "code_changes": {
    "filename.py": "Complete updated file content"
  },
  "confidence_score": 0.85,
  "retry_recommended": true,
  "explanation": "Detailed explanation of the analysis and fixes"
}
"""
        
        return context
    
    async def _query_claude_for_analysis(self, context: str) -> Dict[str, Any]:
        """Query Claude API for failure analysis."""
        try:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                "system": "You are an expert network automation engineer specializing in debugging and fixing Nornir-based network automation workflows. You have deep expertise in network device connectivity, authentication, configuration management, and common automation pitfalls."
            }
            
            response = await self.client.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["content"][0]["text"]
                
                # Extract JSON from Claude's response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    # Fallback parsing
                    return self._parse_text_response(content)
            else:
                logger.error(f"Claude API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Claude API query failed: {str(e)}")
            return {"error": str(e)}
    
    def _parse_claude_response(self, claude_response: Dict[str, Any], fallback_type: str) -> FailureAnalysis:
        """Parse Claude's response into structured FailureAnalysis."""
        if "error" in claude_response:
            return FailureAnalysis(
                failure_type=fallback_type,
                root_cause=f"AI analysis failed: {claude_response['error']}",
                suggested_fixes=["Manual review required"],
                code_changes={},
                confidence_score=0.1,
                retry_recommended=False
            )
        
        return FailureAnalysis(
            failure_type=claude_response.get("failure_type", fallback_type),
            root_cause=claude_response.get("root_cause", "Unknown root cause"),
            suggested_fixes=claude_response.get("suggested_fixes", []),
            code_changes=claude_response.get("code_changes", {}),
            confidence_score=float(claude_response.get("confidence_score", 0.5)),
            retry_recommended=claude_response.get("retry_recommended", True)
        )
    
    def _parse_text_response(self, text_response: str) -> Dict[str, Any]:
        """Fallback parser for non-JSON Claude responses."""
        # Extract key information from text response
        lines = text_response.split('\n')
        
        analysis = {
            "root_cause": "Analysis from text response",
            "failure_type": "unknown",
            "suggested_fixes": [],
            "code_changes": {},
            "confidence_score": 0.6,
            "retry_recommended": True
        }
        
        # Simple text parsing logic
        current_section = None
        for line in lines:
            line = line.strip()
            if "root cause" in line.lower():
                current_section = "root_cause"
            elif "fix" in line.lower() and ":" in line:
                current_section = "fixes"
            elif current_section == "fixes" and line.startswith("-"):
                analysis["suggested_fixes"].append(line[1:].strip())
        
        return analysis
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class FailureAnalysisManager:
    """
    Manages failure analysis workflow and tracks analysis history.
    """
    
    def __init__(self, claude_analyzer: ClaudeFailureAnalyzer):
        """Initialize failure analysis manager."""
        self.analyzer = claude_analyzer
        self.analysis_history: List[Dict[str, Any]] = []
        
    async def analyze_and_suggest_fixes(
        self,
        test_results: Dict[str, Any],
        workflow_code: Dict[str, str],
        environment_info: Dict[str, Any],
        max_attempts: int = 3
    ) -> Tuple[bool, Dict[str, str], List[FailureAnalysis]]:
        """
        Analyze failure and return suggested code fixes.
        
        Args:
            test_results: Failed test results
            workflow_code: Current workflow code
            environment_info: Environment information
            max_attempts: Maximum analysis attempts
            
        Returns:
            Tuple of (should_retry, updated_code, analysis_history)
        """
        analyses = []
        current_code = workflow_code.copy()
        
        for attempt in range(max_attempts):
            logger.info(f"Failure analysis attempt {attempt + 1}/{max_attempts}")
            
            # Get previous attempts for context
            previous_attempts = [
                {
                    "changes_description": f"Attempt {i+1} fixes",
                    "result": "Failed",
                    "error": analysis.root_cause
                }
                for i, analysis in enumerate(analyses)
            ]
            
            # Analyze current failure
            analysis = await self.analyzer.analyze_failure(
                test_results=test_results,
                workflow_code=current_code,
                environment_info=environment_info,
                previous_attempts=previous_attempts
            )
            
            analyses.append(analysis)
            
            # Apply suggested code changes
            if analysis.code_changes and analysis.retry_recommended:
                current_code.update(analysis.code_changes)
                logger.info(f"Applied {len(analysis.code_changes)} code changes")
                
                # Record this attempt
                self.analysis_history.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "attempt": attempt + 1,
                    "analysis": analysis,
                    "code_changes": analysis.code_changes
                })
                
                return True, current_code, analyses
            else:
                logger.warning(f"Analysis suggests no retry (confidence: {analysis.confidence_score})")
                break
        
        return False, current_code, analyses
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of all failure analyses."""
        return {
            "total_analyses": len(self.analysis_history),
            "analysis_history": self.analysis_history,
            "common_failure_types": self._get_common_failure_types(),
            "success_rate": self._calculate_success_rate()
        }
    
    def _get_common_failure_types(self) -> Dict[str, int]:
        """Get frequency of different failure types."""
        failure_counts = {}
        for record in self.analysis_history:
            failure_type = record["analysis"].failure_type
            failure_counts[failure_type] = failure_counts.get(failure_type, 0) + 1
        return failure_counts
    
    def _calculate_success_rate(self) -> float:
        """Calculate success rate of failure analysis fixes."""
        if not self.analysis_history:
            return 0.0
        
        # This would be updated based on actual retry results
        # For now, return based on confidence scores
        total_confidence = sum(
            record["analysis"].confidence_score 
            for record in self.analysis_history
        )
        return total_confidence / len(self.analysis_history) if self.analysis_history else 0.0
