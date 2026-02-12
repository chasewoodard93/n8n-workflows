# 🚀 AI-Powered Network Automation - Deployment Checklist

## ✅ **Code Status: COMPLETE**

All components have been built and integration bugs have been fixed. The system is ready for deployment!

---

## **📋 Pre-Deployment Checklist**

### **1. Prerequisites Installation**

- [ ] **Python 3.10+** installed
  ```bash
  python3 --version  # Should be 3.10 or higher
  ```

- [ ] **Docker** installed (for ContainerLab)
  ```bash
  docker --version
  docker ps  # Verify Docker is running
  ```

- [ ] **ContainerLab** installed (optional, for free virtual devices)
  ```bash
  # Install ContainerLab
  bash -c "$(curl -sL https://get.containerlab.dev)"
  containerlab version
  ```

- [ ] **Terraform** installed (optional, for cloud deployments)
  ```bash
  # Install Terraform
  brew install terraform  # macOS
  # OR
  wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
  unzip terraform_1.5.0_linux_amd64.zip
  sudo mv terraform /usr/local/bin/
  terraform --version
  ```

- [ ] **N8N** installed
  ```bash
  # Option 1: npm
  npm install -g n8n
  
  # Option 2: Docker
  docker pull n8nio/n8n
  ```

- [ ] **Git** installed
  ```bash
  git --version
  ```

---

### **2. API Keys and Credentials**

- [ ] **Claude AI API Key**
  - Sign up: https://console.anthropic.com/
  - Create API key
  - Save securely: `CLAUDE_API_KEY=sk-ant-...`

- [ ] **GitHub Personal Access Token**
  - Go to: GitHub Settings → Developer Settings → Personal Access Tokens
  - Create token with `repo` scope
  - Save securely: `GITHUB_TOKEN=ghp_...`

- [ ] **Slack Webhook URL** (Optional)
  - Go to: https://api.slack.com/apps
  - Create app and enable incoming webhooks
  - Save webhook URL: `SLACK_WEBHOOK_URL=https://hooks.slack.com/...`

- [ ] **Cloud Provider Credentials** (Optional, for licensed devices)
  - **Azure**: Subscription ID, Tenant ID, Client ID, Client Secret
  - **AWS**: Access Key ID, Secret Access Key
  - **GCP**: Service Account JSON

---

### **3. Repository Setup**

- [ ] **Clone/Navigate to Repository**
  ```bash
  cd /Users/admin/Documents/NetScripts/n8n
  ls -la  # Verify structure
  ```

- [ ] **Verify Directory Structure**
  ```
  ✅ enhancements/ai_learning_loop/
  ✅ labflow-automation/
  ✅ nornflow-netops/
  ✅ n8n_workflows/
  ```

---

### **4. LabFlow Configuration**

- [ ] **Create LabFlow Config File**
  ```bash
  cd labflow-automation
  cp config/labflow.yaml.example config/labflow.yaml
  ```

- [ ] **Edit LabFlow Configuration**
  ```bash
  nano config/labflow.yaml
  ```
  
  **Minimum Required Configuration:**
  ```yaml
  api:
    host: 0.0.0.0
    port: 5000
    debug: false

  environments:
    max_concurrent: 5
    default_duration_hours: 2

  containerlab:
    enabled: true
    binary_path: containerlab
    lab_directory: /tmp/labflow-labs

  terraform:
    enabled: true
    binary_path: terraform
    workspace_directory: /tmp/labflow-terraform

  cloud:
    azure:
      subscription_id: ${AZURE_SUBSCRIPTION_ID}
      location: "East US"
    aws:
      region: "us-east-1"
  ```

- [ ] **Install LabFlow Dependencies**
  ```bash
  cd labflow-automation
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- [ ] **Test LabFlow Installation**
  ```bash
  python -m labflow.cli health
  # Expected: ✅ All dependencies available
  ```

---

### **5. AI Learning Loop Configuration**

- [ ] **Create Environment File**
  ```bash
  cd enhancements/ai_learning_loop
  nano .env
  ```
  
  **Required Configuration:**
  ```bash
  # Claude AI
  CLAUDE_API_KEY=your-claude-api-key-here

  # GitHub
  GITHUB_TOKEN=your-github-token-here
  GITHUB_USERNAME=your-github-username
  GITHUB_REPO=network-automation

  # Slack (optional)
  SLACK_WEBHOOK_URL=your-slack-webhook-url
  SLACK_CHANNEL=#automation

  # AI Learning Loop Settings
  MAX_IMPROVEMENT_ATTEMPTS=5
  MIN_CONFIDENCE_THRESHOLD=0.7
  API_HOST=0.0.0.0
  API_PORT=8001
  DEBUG=false

  # LabFlow Configuration Path
  LABFLOW_CONFIG_PATH=../../labflow-automation/config/labflow.yaml

  # Cloud Providers (if using licensed devices)
  AZURE_SUBSCRIPTION_ID=your-azure-subscription-id
  AWS_ACCESS_KEY_ID=your-aws-access-key
  AWS_SECRET_ACCESS_KEY=your-aws-secret-key
  ```

- [ ] **Install AI Learning Loop Dependencies**
  ```bash
  # Use same venv as LabFlow or create new one
  source ../../labflow-automation/venv/bin/activate
  pip install flask flask-cors httpx pyyaml anthropic
  ```

---

### **6. Component Testing**

- [ ] **Test LabFlow API Server**
  ```bash
  cd labflow-automation
  source venv/bin/activate
  python -m labflow.api.server &
  
  # Wait 5 seconds
  sleep 5
  
  # Test health endpoint
  curl http://localhost:5000/health
  # Expected: {"status": "healthy", "services": {...}}
  
  # Stop server
  pkill -f "labflow.api.server"
  ```

- [ ] **Test AI Learning Loop API Server**
  ```bash
  cd enhancements/ai_learning_loop
  source ../../labflow-automation/venv/bin/activate
  set -a; source .env; set +a
  python api_server.py &
  
  # Wait 5 seconds
  sleep 5
  
  # Test health endpoint
  curl http://localhost:8001/health
  # Expected: {"status": "healthy", "services": {...}}
  
  # Stop server
  pkill -f "api_server.py"
  ```

---

### **7. N8N Setup**

- [ ] **Start N8N**
  ```bash
  # Option 1: npm
  n8n start
  
  # Option 2: Docker
  docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
  ```

- [ ] **Access N8N Web Interface**
  - Open browser: http://localhost:5678
  - Create account (first time only)

- [ ] **Import Workflow**
  1. Click "Workflows" in left sidebar
  2. Click "Import from File"
  3. Select: `n8n_workflows/enhanced_ai_learning_workflow.json`
  4. Click "Import"

- [ ] **Configure Workflow Credentials**
  1. Go to Settings → Credentials
  2. Add **Claude API** credential:
     - Type: HTTP Header Auth
     - Name: `x-api-key`
     - Value: Your Claude API key
  3. Add **GitHub** credential:
     - Type: HTTP Header Auth
     - Name: `Authorization`
     - Value: `token your-github-token`
  4. Add **Slack** credential (optional):
     - Type: Slack
     - Webhook URL: Your Slack webhook

- [ ] **Activate Workflow**
  - Click "Active" toggle in top right
  - Workflow should show as "Active"

---

### **8. End-to-End Test**

- [ ] **Start All Services**
  ```bash
  # Terminal 1: LabFlow
  cd labflow-automation
  source venv/bin/activate
  python -m labflow.api.server
  
  # Terminal 2: AI Learning Loop
  cd enhancements/ai_learning_loop
  source ../../labflow-automation/venv/bin/activate
  set -a; source .env; set +a
  python api_server.py
  
  # Terminal 3: N8N (if not already running)
  n8n start
  ```

- [ ] **Run Test Automation**
  1. Get N8N webhook URL from workflow
  2. Open in browser or use form
  3. Fill out test request:
     ```
     Project Name: Test VLAN Config
     Automation Task: Configure VLAN 99 on test switch
     Target Devices: Linux
     Special Requirements: Test only
     ```
  4. Submit and monitor

- [ ] **Monitor Execution**
  - Watch N8N execution log
  - Check LabFlow logs
  - Check AI Learning Loop logs
  - Wait for Slack notification (if configured)

- [ ] **Verify Results**
  - Check GitHub for committed code
  - Review generated automation
  - Verify test results

---

## **🎯 Production Deployment**

Once testing is complete:

- [ ] **Create Systemd Services** (Linux)
- [ ] **Configure Reverse Proxy** (nginx/Apache)
- [ ] **Set Up SSL Certificates**
- [ ] **Configure Firewall Rules**
- [ ] **Set Up Monitoring**
- [ ] **Configure Backups**
- [ ] **Document Runbooks**
- [ ] **Train Team**

---

## **📊 Success Criteria**

✅ All health checks passing
✅ Test automation completes successfully
✅ Code committed to GitHub
✅ Slack notifications received (if configured)
✅ No errors in logs
✅ All services stable

---

## **🆘 Troubleshooting**

If issues occur, check:
1. All environment variables set correctly
2. All services running on correct ports
3. No port conflicts
4. API keys valid
5. Network connectivity
6. Log files for errors

See `COMPLETE_DOCUMENTATION.md` for detailed troubleshooting guide.

