# 🎯 Getting Started - Detailed Step-by-Step Guide

**Complete guide to set up and test the AI-powered network automation workflow generator**

---

## **📋 Prerequisites Checklist**

Before you start, make sure you have:

- [ ] **Docker installed** - [Download here](https://docs.docker.com/get-docker/)
  - Verify: Run `docker --version` in terminal
  - Expected: `Docker version 20.10.x` or higher

- [ ] **Anthropic API Key** - [Get one here](https://console.anthropic.com/)
  - Sign up for Anthropic account
  - Go to API Keys section
  - Create new API key
  - Copy and save it somewhere safe

- [ ] **Repository cloned** - Run this command:
  ```bash
  git clone https://github.com/chasewoodard93/n8n-network-automation.git
  cd n8n-network-automation
  ```

- [ ] **Basic terminal knowledge** - Comfortable running commands

- [ ] **Text editor** - VS Code, Sublime, or any editor

- [ ] **Email address** - For test notifications

---

## **⚡ STEP 1: Start N8N with Docker (5 minutes)**

### **1.1 Create N8N Data Directory**

This directory stores N8N data so it persists between restarts.

**macOS/Linux:**
```bash
mkdir -p ~/.n8n
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.n8n"
```

### **1.2 Start N8N Container**

**macOS/Linux:**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n
```

**Windows (PowerShell):**
```powershell
docker run -d `
  --name n8n `
  -p 5678:5678 `
  -v "$env:USERPROFILE\.n8n:/home/node/.n8n" `
  --restart unless-stopped `
  n8nio/n8n
```

### **1.3 Verify N8N is Running**

```bash
docker ps | grep n8n
```

**Expected output:**
```
CONTAINER ID   IMAGE       STATUS          PORTS
abc123def456   n8nio/n8n   Up 10 seconds   0.0.0.0:5678->5678/tcp
```

**If you don't see this:**
```bash
# Check logs for errors
docker logs n8n

# If port 5678 is in use, use different port
docker run -d --name n8n -p 5679:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
# Then access at http://localhost:5679
```

### **1.4 Wait for N8N to Start**

N8N takes 30-60 seconds to fully start. Wait and then:

```bash
# Check if N8N is ready
curl http://localhost:5678

# Should return HTML (not an error)
```

---

## **🌐 STEP 2: Access N8N Web Interface (5 minutes)**

### **2.1 Open N8N in Browser**

Open your browser and go to:
```
http://localhost:5678
```

**Expected screen:** N8N setup wizard

### **2.2 Complete Initial Setup**

**Screen 1: Welcome**
- Click "Start" or "Get Started"

**Screen 2: Create Admin Account**
- **Email:** Use any email (e.g., `admin@localhost`)
- **Password:** Create a strong password
- **First Name:** Your name (or "Admin")
- **Last Name:** Your name (or "User")
- Click "Next"

**Screen 3: Workspace Setup**
- **Workspace Name:** "My Network Automation"
- Click "Next"

**Screen 4: Invite Team**
- Skip this (click "Skip" or "Continue")

**Expected result:** You're now in the N8N dashboard

### **2.3 Verify Dashboard**

You should see:
- Left sidebar with "Workflows", "Credentials", "Settings"
- Main area showing "Workflows" section
- Top right showing your user icon

**Screenshot description:**
- Clean interface with dark/light theme option
- "New" button in top left
- Search bar at top
- Empty workflows list

---

## **📥 STEP 3: Import the Workflow File (5 minutes)**

### **3.1 Locate the Workflow File**

In your cloned repository:
```
n8n-network-automation/
└── n8n-workflows/
    └── network_stack_generator.json
```

### **3.2 Import into N8N**

**Method 1: Using N8N UI (Recommended)**

1. Click **"Workflows"** in left sidebar
2. Click **"New"** button (top left)
3. Click **"Import from File"** (or look for import option)
4. Select `n8n-workflows/network_stack_generator.json`
5. Click **"Import"**

**Expected result:** Workflow appears in your workflows list

**Method 2: Using Menu**

1. Click **"Workflows"** in left sidebar
2. Look for **"Import"** or **"Upload"** button
3. Select the JSON file
4. Click **"Import"**

### **3.3 Verify Import Success**

1. Click on the imported workflow (should be named "Network Stack Generator")
2. You should see the workflow canvas with nodes
3. Look for these nodes:
   - Form Trigger
   - Parse Form Data
   - AI Agent 1: Workflow Generator
   - AI Agent 2: Testing Agent
   - AI Agent 3: Validation Agent
   - Package & Deliver

**If import fails:**
```bash
# Check file exists
ls -la n8n-workflows/network_stack_generator.json

# Check file is valid JSON
cat n8n-workflows/network_stack_generator.json | head -20
```

---

## **🔑 STEP 4: Configure Anthropic API Credentials (10 minutes)**

### **4.1 Add Credentials to N8N**

1. Click **"Credentials"** in left sidebar
2. Click **"New"** button
3. Search for **"HTTP Request"** or **"Anthropic"**
4. Select **"HTTP Request"** (we'll use this for API calls)
5. Name it: `Anthropic API`
6. Click **"Create"**

### **4.2 Configure Each AI Agent Node**

**For AI Agent 1 (Workflow Generator):**

1. Open the workflow (click on "Network Stack Generator")
2. Double-click on **"AI Agent 1: Workflow Generator"** node
3. Look for **"Authentication"** or **"Headers"** section
4. Add header:
   - **Key:** `Authorization`
   - **Value:** `Bearer YOUR_ANTHROPIC_API_KEY`
5. Replace `YOUR_ANTHROPIC_API_KEY` with your actual key from https://console.anthropic.com/
6. Click **"Save"**

**For AI Agent 2 (Testing Agent):**

1. Double-click on **"AI Agent 2: Testing Agent"** node
2. Add same header with your API key
3. Click **"Save"**

**For AI Agent 3 (Validation Agent):**

1. Double-click on **"AI Agent 3: Validation Agent"** node
2. Add same header with your API key
3. Click **"Save"**

### **4.3 Test API Connection**

1. In any AI Agent node, click **"Test"** button
2. Should see: `✓ Connection successful` or similar
3. If error, check:
   - API key is correct
   - No extra spaces in key
   - Key is from https://console.anthropic.com/

---

## **✅ STEP 5: Activate the Workflow (5 minutes)**

### **5.1 Activate**

1. Open the workflow (click "Network Stack Generator")
2. Look for **"Active"** toggle in top right
3. Click to turn it **ON** (should turn green)
4. You should see: "Workflow is now active"

### **5.2 Get the Form URL**

1. In the workflow, find the **"Form Trigger"** node
2. Click on it
3. Look for **"Test URL"** or **"Production URL"**
4. Copy the URL (looks like: `http://localhost:5678/form/abc123def456`)

### **5.3 Verify Workflow is Active**

```bash
# Check N8N logs
docker logs n8n | tail -20

# Should show workflow is active
```

---

## **🧪 STEP 6: Test with Sample Data (10 minutes)**

### **6.1 Access the Form**

1. Copy the form URL from Step 5.2
2. Open in new browser tab
3. You should see a web form with fields

### **6.2 Fill Form with Sample Data**

**Project Information:**
```
Project Name: my-first-automation
Company Name: Acme Corp
```

**Network Devices:**
```
Device Type: switch
Vendor: cisco
Model: Catalyst 9300
Platform: ios
Quantity: 5
IP Range Start: 192.168.1.10
Site: datacenter-1
Role: access
```

**Workflows to Generate:**
- ✅ Check "Backup Devices"
- ✅ Check "Configuration Deployment"

**Integrations (Optional):**
- NetBox URL: (leave blank for now)
- Git Repository: (leave blank for now)

**Email:**
```
your-email@example.com
```

### **6.3 Submit Form**

1. Click **"Submit"** button
2. You should see: "Form submitted successfully"
3. Go back to N8N window

### **6.4 Monitor Workflow Execution**

1. In N8N, click **"Executions"** tab
2. You should see a new execution running
3. Watch the nodes execute:
   - Form Trigger (green checkmark)
   - Parse Form Data (green checkmark)
   - AI Agent 1 (running... then green checkmark)
   - AI Agent 2 (running... then green checkmark)
   - AI Agent 3 (running... then green checkmark)
   - Package & Deliver (running... then green checkmark)

**Expected time:** 2-5 minutes

---

## **🔍 STEP 7: Verify AI Agents Are Working (5 minutes)**

### **7.1 Check Execution Details**

1. Click on the completed execution
2. Click on **"AI Agent 1: Workflow Generator"** node
3. Look for **"Output"** section
4. You should see generated YAML workflow

**Expected output:**
```yaml
workflow:
  name: "Backup Network Devices"
  description: "Automated backup of Cisco Catalyst 9300 switches"
  failure_strategy: "skip-failed"
  tasks:
    - name: test_connectivity
      task: test_connectivity
    - name: backup_config
      task: backup_config
    ...
```

### **7.2 Check AI Agent 2 Output**

1. Click on **"AI Agent 2: Testing Agent"** node
2. Look for **"Output"** section
3. You should see generated Python test code

**Expected output:**
```python
import pytest
from unittest.mock import Mock, patch

class TestBackupWorkflow:
    def test_workflow_yaml_valid(self):
        assert True
    
    def test_connectivity_check(self):
        assert True
    ...
```

### **7.3 Check AI Agent 3 Output**

1. Click on **"AI Agent 3: Validation Agent"** node
2. Look for **"Output"** section
3. You should see validation results

**Expected output:**
```json
{
  "status": "valid",
  "checks_passed": 10,
  "checks_failed": 0,
  "issues": [],
  "recommendations": []
}
```

### **7.4 Check Email Notification**

1. Check your email (the one you entered in the form)
2. Look for email from N8N
3. Subject: "Your Network Automation Stack is Ready!"
4. Contains download link to ZIP file

---

## **✨ STEP 8: Success Verification Checklist**

Go through this checklist to verify everything is working:

- [ ] **N8N Running**
  - `docker ps | grep n8n` shows container running
  - Can access http://localhost:5678

- [ ] **Workflow Imported**
  - Workflow appears in "Workflows" list
  - All nodes visible in canvas
  - No import errors

- [ ] **API Credentials Configured**
  - All three AI Agent nodes have API key
  - Test connection passes
  - No authentication errors

- [ ] **Workflow Activated**
  - "Active" toggle is ON (green)
  - Form URL is accessible
  - Can open form in browser

- [ ] **Form Submission Works**
  - Can fill and submit form
  - No validation errors
  - Sees success message

- [ ] **Workflow Executes**
  - Execution appears in "Executions" tab
  - All nodes turn green (success)
  - Takes 2-5 minutes to complete

- [ ] **AI Agents Generate Content**
  - AI Agent 1 output contains YAML workflow
  - AI Agent 2 output contains Python tests
  - AI Agent 3 output contains validation results

- [ ] **Email Notification Received**
  - Email arrives within 5 minutes
  - Contains download link
  - Subject mentions "Network Automation Stack"

- [ ] **Generated Files Available**
  - Can download ZIP file from email
  - ZIP contains workflows, tests, inventory
  - Files are valid (can open and read)

---

## **🚀 STEP 9: Next Steps**

### **Option 1: Generate More Workflows**

1. Go back to form URL
2. Change settings (e.g., select different workflows)
3. Submit again
4. Get new generated workflows

### **Option 2: Customize Generated Workflows**

1. Download the ZIP file from email
2. Extract it
3. Edit `workflows/backup_devices.yaml`
4. Add custom tasks or change settings
5. Run with NornFlow: `nornflow run workflows/backup_devices.yaml`

### **Option 3: Set Up Real Network Devices**

1. Update `inventory/hosts.yaml` with real device IPs
2. Add credentials to `.env` file
3. Run workflow: `nornflow run workflows/backup_devices.yaml`

### **Option 4: Add Integrations**

1. Edit workflow YAML
2. Add NetBox, ServiceNow, Grafana configs
3. Set environment variables for credentials
4. Run workflow with integrations enabled

---

## **🔧 Troubleshooting**

### **Issue: N8N won't start**

**Error:** `docker: Error response from daemon`

**Fix:**
```bash
# Check if port is in use
lsof -i :5678

# If in use, kill the process or use different port
docker run -d --name n8n -p 5679:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

### **Issue: Can't access http://localhost:5678**

**Error:** `Connection refused`

**Fix:**
```bash
# Check if container is running
docker ps | grep n8n

# If not running, start it
docker start n8n

# Check logs
docker logs n8n
```

### **Issue: API key not working**

**Error:** `401 Unauthorized` or `Invalid API key`

**Fix:**
1. Go to https://console.anthropic.com/
2. Verify API key is correct
3. Check for extra spaces in key
4. Try creating new API key
5. Update all three AI Agent nodes

### **Issue: Form submission fails**

**Error:** `Form submission error` or blank page

**Fix:**
```bash
# Check N8N logs
docker logs n8n | tail -50

# Look for error messages
# Common issues:
# - API key not configured
# - Workflow not active
# - Node configuration error
```

### **Issue: AI agents not generating content**

**Error:** Empty output or error messages

**Fix:**
1. Check API key is valid
2. Check API key has credits
3. Check node configuration
4. Try submitting form again
5. Check N8N logs for errors

---

## **📚 Learn More**

- [Complete Architecture Guide](N8N_AI_WORKFLOW_ARCHITECTURE.md)
- [Quick Start Guide](QUICK_START_GUIDE.md)
- [N8N Setup Guide](N8N_SETUP_COMPLETE_GUIDE.md)
- [NornFlow Installation](NORNFLOW_INSTALLATION_GUIDE.md)

---

## **🎉 You're Done!**

You now have a fully functional AI-powered network automation workflow generator!

**Next:** Generate your first workflow and deploy it to your network! 🚀

