#!/usr/bin/env python3
"""
API Server for AI Learning Loop.

Provides REST API endpoints for the iterative improvement engine
to be called from N8N workflows.
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from enhancements.ai_learning_loop.iterative_improver import IterativeImprovementEngine
from enhancements.github_integration import GitHubManager
from enhancements.slack_integration import SlackNotifier

# Import LabFlow from correct path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'labflow-automation'))
from labflow.core.manager import LabFlowManager
from labflow.utils.config import Config as LabFlowConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global instances
improvement_engine: Optional[IterativeImprovementEngine] = None
labflow_manager: Optional[LabFlowManager] = None


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables and config files."""
    config = {
        "claude_api_key": os.getenv("CLAUDE_API_KEY"),
        "github_token": os.getenv("GITHUB_TOKEN"),
        "github_username": os.getenv("GITHUB_USERNAME"),
        "github_repo": os.getenv("GITHUB_REPO", "network-automation"),
        "slack_webhook_url": os.getenv("SLACK_WEBHOOK_URL"),
        "slack_channel": os.getenv("SLACK_CHANNEL", "#automation"),
        "max_improvement_attempts": int(os.getenv("MAX_IMPROVEMENT_ATTEMPTS", "5")),
        "min_confidence_threshold": float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.7")),
        "labflow_config_path": os.getenv("LABFLOW_CONFIG_PATH", "../labflow-automation/config/labflow.yaml")
    }
    
    # Validate required configuration
    required_keys = ["claude_api_key", "github_token", "github_username"]
    missing_keys = [key for key in required_keys if not config[key]]
    
    if missing_keys:
        raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")
    
    return config


async def initialize_services():
    """Initialize all services and managers."""
    global improvement_engine, labflow_manager
    
    try:
        logger.info("Initializing AI Learning Loop services...")
        
        # Load configuration
        config = load_config()
        
        # Initialize GitHub manager
        github_manager = GitHubManager(
            token=config["github_token"],
            username=config["github_username"],
            repo=config["github_repo"]
        )
        
        # Initialize Slack notifier
        slack_notifier = SlackNotifier(
            webhook_url=config["slack_webhook_url"],
            default_channel=config["slack_channel"]
        )
        
        # Initialize LabFlow manager
        labflow_config_path = config["labflow_config_path"]
        if os.path.exists(labflow_config_path):
            logger.info(f"Loading LabFlow config from: {labflow_config_path}")
            labflow_config = LabFlowConfig(config_file=labflow_config_path)
        else:
            logger.warning(f"LabFlow config not found at {labflow_config_path}, using defaults")
            # Create default LabFlow configuration
            labflow_config = LabFlowConfig()

        labflow_manager = LabFlowManager(labflow_config)
        
        # Initialize improvement engine
        improvement_engine = IterativeImprovementEngine(
            claude_api_key=config["claude_api_key"],
            github_manager=github_manager,
            slack_notifier=slack_notifier,
            max_improvement_attempts=config["max_improvement_attempts"],
            min_confidence_threshold=config["min_confidence_threshold"]
        )
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "improvement_engine": improvement_engine is not None,
            "labflow_manager": labflow_manager is not None
        }
    })


@app.route("/api/improve-until-success", methods=["POST"])
def improve_until_success():
    """
    Main endpoint for AI learning loop.
    
    Accepts workflow code and iteratively improves it until tests pass.
    """
    try:
        if not improvement_engine or not labflow_manager:
            return jsonify({
                "success": False,
                "error": "Services not initialized"
            }), 500
        
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        # Validate required fields
        required_fields = ["workflow_name", "initial_code", "environment_config", "user_requirements"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Extract parameters
        workflow_name = data["workflow_name"]
        initial_code = data["initial_code"]
        environment_config = data["environment_config"]
        user_requirements = data["user_requirements"]
        project_id = data.get("project_id", f"ai-improvement-{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}")
        
        logger.info(f"Starting improvement session for workflow: {workflow_name}")
        
        # Run improvement loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            session_result = loop.run_until_complete(
                improvement_engine.improve_until_success(
                    workflow_name=workflow_name,
                    initial_code=initial_code,
                    labflow_manager=labflow_manager,
                    environment_config=environment_config,
                    user_requirements=user_requirements,
                    project_id=project_id
                )
            )
            
            # Return session results
            return jsonify({
                "success": True,
                "session_id": session_result["session_id"],
                "workflow_name": session_result["workflow_name"],
                "final_status": session_result["final_status"],
                "attempts": session_result["attempts"],
                "duration_minutes": session_result.get("duration_minutes", 0),
                "final_code": session_result.get("final_code"),
                "commit_result": session_result.get("commit_result"),
                "environment_id": session_result.get("environment_id")
            })
        
        finally:
            loop.close()
    
    except Exception as e:
        logger.error(f"Improvement session failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/improvement-stats", methods=["GET"])
def get_improvement_stats():
    """Get statistics about improvement sessions."""
    try:
        if not improvement_engine:
            return jsonify({
                "success": False,
                "error": "Improvement engine not initialized"
            }), 500
        
        stats = improvement_engine.get_improvement_statistics()
        
        return jsonify({
            "success": True,
            "statistics": stats
        })
    
    except Exception as e:
        logger.error(f"Failed to get improvement stats: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/sessions", methods=["GET"])
def list_improvement_sessions():
    """List all improvement sessions."""
    try:
        if not improvement_engine:
            return jsonify({
                "success": False,
                "error": "Improvement engine not initialized"
            }), 500
        
        sessions = improvement_engine.improvement_sessions
        
        # Return summary information (not full session data)
        session_summaries = []
        for session in sessions:
            session_summaries.append({
                "session_id": session["session_id"],
                "workflow_name": session["workflow_name"],
                "start_time": session["start_time"],
                "end_time": session.get("end_time"),
                "final_status": session["final_status"],
                "attempts_count": len(session["attempts"]),
                "duration_minutes": session.get("duration_minutes", 0)
            })
        
        return jsonify({
            "success": True,
            "sessions": session_summaries,
            "total_sessions": len(session_summaries)
        })
    
    except Exception as e:
        logger.error(f"Failed to list sessions: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/sessions/<session_id>", methods=["GET"])
def get_session_details(session_id: str):
    """Get detailed information about a specific session."""
    try:
        if not improvement_engine:
            return jsonify({
                "success": False,
                "error": "Improvement engine not initialized"
            }), 500
        
        # Find session by ID
        session = None
        for s in improvement_engine.improvement_sessions:
            if s["session_id"] == session_id:
                session = s
                break
        
        if not session:
            return jsonify({
                "success": False,
                "error": f"Session {session_id} not found"
            }), 404
        
        return jsonify({
            "success": True,
            "session": session
        })
    
    except Exception as e:
        logger.error(f"Failed to get session details: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


def main():
    """Main entry point."""
    try:
        # Initialize services
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_services())
        loop.close()
        
        # Start Flask server
        host = os.getenv("API_HOST", "0.0.0.0")
        port = int(os.getenv("API_PORT", "8001"))
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        logger.info(f"Starting AI Learning Loop API server on {host}:{port}")
        
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
