# 🤖 **AI Learning Loop Setup Guide**

## **🎯 Overview**

The AI Learning Loop is an intelligent system that automatically:
1. **Generates** network automation code with Claude AI
2. **Tests** the code in LabFlow environments  
3. **Analyzes** failures with AI-powered root cause analysis
4. **Fixes** issues automatically by regenerating improved code
5. **Repeats** until all tests pass
6. **Commits** successful automation to GitHub
7. **Notifies** team via Slack

## **🏗️ Architecture**

```
User Input → N8N Form → Claude AI → AI Learning Loop → LabFlow → Testing
                                         ↓
GitHub ← Commit Success ← All Tests Pass ← Fix & Retry ← Failure Analysis
                                         ↓
                                    Slack Notifications
```

## **📋 Prerequisites**

### **Required Services**
- **Claude AI API**: For code generation and failure analysis
- **LabFlow**: For test environment creation and management
- **GitHub**: For code repository and version control
- **Slack**: For team notifications (optional)
- **N8N**: For workflow orchestration

### **Required API Keys**
```bash
# Claude AI
CLAUDE_API_KEY="your-claude-api-key"

# GitHub
GITHUB_TOKEN="your-github-personal-access-token"
GITHUB_USERNAME="your-github-username"
GITHUB_REPO="network-automation"

# Slack (optional)
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
SLACK_CHANNEL="#automation"

# Configuration
MAX_IMPROVEMENT_ATTEMPTS="5"
MIN_CONFIDENCE_THRESHOLD="0.7"
```

## **🚀 Installation**

### **1. Install Dependencies**
```bash
cd enhancements/ai_learning_loop
pip install -r requirements.txt
```

### **2. Create Requirements File**
```bash
cat > requirements.txt << EOF
flask>=2.3.0
flask-cors>=4.0.0
httpx>=0.24.0
pyyaml>=6.0
asyncio
dataclasses
typing
datetime
logging
base64
json
os
sys
EOF
```

### **3. Set Environment Variables**
```bash
# Create environment file
cat > .env << EOF
CLAUDE_API_KEY=your-claude-api-key-here
GITHUB_TOKEN=your-github-token-here
GITHUB_USERNAME=your-github-username
GITHUB_REPO=network-automation
SLACK_WEBHOOK_URL=your-slack-webhook-url
SLACK_CHANNEL=#automation
MAX_IMPROVEMENT_ATTEMPTS=5
MIN_CONFIDENCE_THRESHOLD=0.7
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=false
LABFLOW_CONFIG_PATH=../labflow-automation/config/labflow.yaml
EOF

# Load environment variables
source .env
export $(cat .env | xargs)
```

### **4. Start AI Learning Loop API Server**
```bash
python api_server.py
```

The server will start on `http://localhost:8001`

## **🔧 Configuration**

### **LabFlow Integration**
Ensure LabFlow is running and accessible:
```bash
# Start LabFlow (in separate terminal)
cd ../labflow-automation
python -m labflow.api.server
```

### **N8N Workflow Setup**
1. Import the enhanced workflow: `n8n_workflows/enhanced_ai_learning_workflow.json`
2. Configure N8N variables:
   ```
   claude_api_key: Your Claude API key
   improvement_api_key: API key for learning loop (optional)
   github_username: Your GitHub username
   github_repo: Target repository name
   github_token: GitHub personal access token
   slack_channel: Slack notification channel
   max_improvement_attempts: Maximum retry attempts (default: 5)
   ```

## **📊 API Endpoints**

### **Main Improvement Endpoint**
```http
POST /api/improve-until-success
Content-Type: application/json

{
  "workflow_name": "vlan-configuration",
  "initial_code": {
    "main.py": "# Generated Python code...",
    "inventory/hosts.yaml": "# Nornir inventory...",
    "requirements.txt": "# Dependencies..."
  },
  "environment_config": {
    "environment_type": "auto",
    "device_types": ["Cisco IOS", "Linux"],
    "topology_requirements": {}
  },
  "user_requirements": "Configure VLANs on all switches",
  "project_id": "vlan-automation-2024"
}
```

### **Statistics and Monitoring**
```http
GET /api/improvement-stats
GET /api/sessions
GET /api/sessions/{session_id}
GET /health
```

## **🎮 Usage Workflow**

### **1. User Submits Request**
- Fill out N8N form with automation requirements
- Specify target device types and special requirements
- Submit form to trigger workflow

### **2. AI Code Generation**
- Claude AI analyzes requirements
- Generates complete Nornir automation code
- Creates inventory files, templates, and documentation

### **3. AI Learning Loop Begins**
- Creates test environment in LabFlow
- Tests generated code against real/virtual devices
- If tests fail:
  - Analyzes failure with Claude AI
  - Generates improved code
  - Re-tests with fixes
  - Repeats until success or max attempts

### **4. Success Actions**
- Commits working code to GitHub
- Creates detailed commit message with improvement history
- Notifies team via Slack with results
- Provides links to repository and test results

## **🔍 Monitoring and Debugging**

### **Log Files**
```bash
# API server logs
tail -f logs/ai_learning_loop.log

# LabFlow logs  
tail -f ../labflow-automation/logs/labflow.log
```

### **Health Checks**
```bash
# Check API server health
curl http://localhost:8001/health

# Check improvement statistics
curl http://localhost:8001/api/improvement-stats
```

### **Session Monitoring**
```bash
# List all improvement sessions
curl http://localhost:8001/api/sessions

# Get detailed session information
curl http://localhost:8001/api/sessions/{session_id}
```

## **🛠️ Troubleshooting**

### **Common Issues**

#### **1. Claude API Errors**
```bash
# Check API key
echo $CLAUDE_API_KEY

# Test API connectivity
curl -H "x-api-key: $CLAUDE_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.anthropic.com/v1/messages
```

#### **2. LabFlow Connection Issues**
```bash
# Check LabFlow status
curl http://localhost:5000/health

# Verify LabFlow configuration
cat ../labflow-automation/config/labflow.yaml
```

#### **3. GitHub Integration Problems**
```bash
# Test GitHub token
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user

# Check repository access
curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/$GITHUB_USERNAME/$GITHUB_REPO
```

#### **4. Environment Creation Failures**
- Check device type availability in LabFlow
- Verify cloud provider credentials (Azure/AWS)
- Ensure sufficient resource quotas

### **Debug Mode**
```bash
# Start API server in debug mode
DEBUG=true python api_server.py

# Enable verbose logging
export LOG_LEVEL=DEBUG
```

## **📈 Performance Optimization**

### **Concurrent Sessions**
- Default: 3 concurrent improvement sessions
- Adjust based on LabFlow capacity and cloud quotas
- Monitor resource usage during peak times

### **Timeout Configuration**
```python
# Adjust timeouts in api_server.py
improvement_timeout = 1800  # 30 minutes
environment_creation_timeout = 600  # 10 minutes
test_execution_timeout = 300  # 5 minutes
```

### **Cost Optimization**
- Use ContainerLab for free devices when possible
- Set appropriate environment expiration times
- Monitor cloud resource usage
- Implement resource cleanup policies

## **🔒 Security Considerations**

### **API Security**
- Use HTTPS in production
- Implement API key authentication
- Rate limiting for API endpoints
- Input validation and sanitization

### **Credential Management**
- Store API keys in secure environment variables
- Use secrets management systems (HashiCorp Vault, etc.)
- Rotate credentials regularly
- Audit access logs

### **Network Security**
- Firewall rules for API server
- VPN access for LabFlow environments
- Secure communication between services

## **🎉 Success Metrics**

### **Key Performance Indicators**
- **Success Rate**: Percentage of automations that pass after improvement
- **Average Attempts**: Number of improvement iterations needed
- **Time to Success**: Duration from start to working automation
- **Cost per Automation**: Cloud resources used per successful automation

### **Quality Metrics**
- **Test Coverage**: Percentage of automation features tested
- **Failure Analysis Accuracy**: AI's ability to identify root causes
- **Fix Success Rate**: Percentage of AI-generated fixes that work

## **🚀 Ready for Production!**

Your AI Learning Loop is now configured and ready to automatically generate, test, and improve network automation workflows!

**Next Steps:**
1. Test with simple automation requirements
2. Monitor improvement sessions and success rates
3. Adjust configuration based on results
4. Scale up for production workloads

**The future of network automation is here - intelligent, self-improving, and fully automated!** 🤖✨
