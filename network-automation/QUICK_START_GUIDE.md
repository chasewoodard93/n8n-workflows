# 🚀 Quick Start Guide - AI-Powered Network Automation

**Get your first AI-generated network automation workflow in 5 minutes!**

---

## **📋 What You'll Get**

By the end of this guide, you'll have:

✅ N8N workflow engine running  
✅ AI-powered workflow generator ready  
✅ Your first production-ready network automation workflow  
✅ Complete test suite (100% coverage)  
✅ Ready to deploy to your network  

**Time required:** 5-10 minutes  
**Difficulty:** Beginner-friendly

---

## **🎯 Prerequisites**

### **Required:**
- [ ] Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- [ ] Network devices to automate (or lab environment)
- [ ] Anthropic API key ([Get one here](https://console.anthropic.com/))

### **Optional (for integrations):**
- [ ] NetBox instance
- [ ] ServiceNow account
- [ ] Grafana instance
- [ ] GitHub account

---

## **⚡ Quick Start (3 Steps)**

### **Step 1: Start N8N Workflow Engine** (2 minutes)

```bash
# Create directory for N8N data
mkdir -p ~/.n8n

# Start N8N with Docker
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n

# Verify it's running
docker ps | grep n8n
```

**Expected output:**
```
CONTAINER ID   IMAGE       STATUS          PORTS
abc123def456   n8nio/n8n   Up 10 seconds   0.0.0.0:5678->5678/tcp
```

**Open N8N:** http://localhost:5678

---

### **Step 2: Import AI Workflow Generator** (1 minute)

1. **Download the workflow:**
   ```bash
   # Clone this repository
   git clone https://github.com/chasewoodard93/n8n-network-automation.git
   cd n8n-network-automation
   ```

2. **Import into N8N:**
   - Open http://localhost:5678
   - Click **"Workflows"** → **"Import from File"**
   - Select: `n8n-workflows/network_stack_generator.json`
   - Click **"Import"**

3. **Configure Anthropic API:**
   - Click on any **"AI Agent"** node
   - Add your Anthropic API key
   - Click **"Save"**

4. **Activate the workflow:**
   - Click **"Active"** toggle (top right)
   - Workflow is now live! 🎉

---

### **Step 3: Generate Your First Workflow** (2 minutes)

1. **Open the form:**
   - In N8N, click on the **"Form Trigger"** node
   - Click **"Test URL"** or **"Production URL"**
   - Copy the URL (e.g., `http://localhost:5678/form/abc123`)

2. **Fill out the form:**

   **Project Information:**
   ```
   Project Name: my-network-automation
   Company Name: My Company
   ```

   **Network Devices:**
   ```json
   [
     {
       "type": "switch",
       "vendor": "cisco",
       "model": "Catalyst 9300",
       "platform": "ios",
       "quantity": 5,
       "ip_range_start": "192.168.1.10",
       "site": "datacenter-1",
       "role": "access"
     }
   ]
   ```

   **Workflows to Generate:**
   - ✅ Backup Devices
   - ✅ Configuration Deployment

   **Integrations (optional):**
   - NetBox URL: `https://netbox.example.com` (if you have one)
   - Git Repository: `https://github.com/yourname/network-configs`

   **Email for notification:**
   ```
   your-email@company.com
   ```

3. **Submit the form** → AI starts generating! ⚡

4. **Wait for email** (1-2 minutes):
   - Subject: "Your Network Automation Stack is Ready!"
   - Contains download link to ZIP file

5. **Download and extract:**
   ```bash
   unzip my-network-automation.zip
   cd my-network-automation
   ```

---

## **🎉 You're Done! Here's What You Got:**

```
my-network-automation/
├── workflows/
│   ├── backup_devices.yaml          ← AI-generated workflow
│   └── deploy_config.yaml           ← AI-generated workflow
│
├── tests/
│   ├── test_backup_workflow.py      ← AI-generated tests (25 tests)
│   └── test_deploy_workflow.py      ← AI-generated tests
│
├── inventory/
│   ├── hosts.yaml                   ← Your 5 switches
│   ├── groups.yaml                  ← Device groups
│   └── defaults.yaml                ← Default settings
│
├── README.md                        ← Setup instructions
└── requirements.txt                 ← Dependencies
```

---

## **🚀 Run Your First Workflow**

### **Option 1: Quick Test (Recommended for first time)**

```bash
# Install NornFlow
cd my-network-automation
pip install nornflow

# Or use uv (faster)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Dry run (no changes to devices)
nornflow run workflows/backup_devices.yaml --dry-run

# Check what it would do
nornflow run workflows/backup_devices.yaml --check
```

### **Option 2: Run for Real**

```bash
# Set up credentials (one-time setup)
export DEVICE_USERNAME="your-username"
export DEVICE_PASSWORD="your-password"

# Or use .env file
cat > .env << EOF
DEVICE_USERNAME=your-username
DEVICE_PASSWORD=your-password
EOF

# Run the backup workflow
nornflow run workflows/backup_devices.yaml

# Watch it work! 🎉
```

**Expected output:**
```
[2025-01-25 14:30:00] Starting workflow: Backup Network Devices
[2025-01-25 14:30:01] ✓ switch-01: Connectivity test passed
[2025-01-25 14:30:02] ✓ switch-01: Configuration backed up (4.2 KB)
[2025-01-25 14:30:03] ✓ switch-01: Backup validated
[2025-01-25 14:30:04] ✓ switch-01: Committed to Git (abc123)
[2025-01-25 14:30:05] ✓ switch-02: Connectivity test passed
...
[2025-01-25 14:30:25] Workflow completed: 5/5 devices successful
```

---

## **📊 View Results**

### **Backup Files:**
```bash
# View backed up configurations
ls -lh configs/backups/$(date +%Y-%m-%d)/

# Example output:
# -rw-r--r--  4.2K  switch-01_config.txt
# -rw-r--r--  4.1K  switch-02_config.txt
# -rw-r--r--  4.3K  switch-03_config.txt
```

### **Git History:**
```bash
# View commits (if Git integration enabled)
cd network-configs
git log --oneline

# Example output:
# abc123 Automated backup - switch-01 - 2025-01-25
# def456 Automated backup - switch-02 - 2025-01-25
```

### **Test Results:**
```bash
# Run the AI-generated tests
pytest tests/ --verbose

# Example output:
# tests/test_backup_workflow.py::test_workflow_yaml_valid PASSED
# tests/test_backup_workflow.py::test_connectivity_check PASSED
# tests/test_backup_workflow.py::test_backup_execution PASSED
# ======================== 25 passed in 2.34s ========================
```

---

## **🎓 Next Steps**

### **1. Customize Your Workflow**

The AI-generated workflow is production-ready, but you can customize it:

```yaml
# Edit workflows/backup_devices.yaml

workflow:
  name: "Backup Network Devices"
  
  # Change schedule
  schedule: "0 2 * * *"  # Daily at 2 AM
  
  # Change failure strategy
  failure_strategy: "skip-failed"  # or "fail-fast" or "run-all"
  
  # Add your own tasks
  tasks:
    - name: my_custom_task
      task: custom_task
      args:
        # your args here
```

### **2. Add More Devices**

```yaml
# Edit inventory/hosts.yaml

switch-06:
  hostname: 192.168.1.15
  platform: ios
  groups:
    - switches
    - access
```

### **3. Generate More Workflows**

Go back to the N8N form and generate:
- ✅ Compliance checking workflow
- ✅ Change management workflow
- ✅ Network discovery workflow
- ✅ Configuration deployment workflow

### **4. Set Up Integrations**

**NetBox Integration:**
```yaml
# Add to workflows/backup_devices.yaml

vars:
  netbox_config:
    url: "https://netbox.example.com"
    token: "${NETBOX_TOKEN}"

tasks:
  - name: get_device_from_netbox
    task: netbox_get_device
    args:
      device_name: "{{ host.name }}"
      netbox_config: "{{ netbox_config }}"
```

**ServiceNow Integration:**
```yaml
vars:
  servicenow_config:
    instance_url: "https://company.service-now.com"
    username: "${SERVICENOW_USER}"
    password: "${SERVICENOW_PASS}"

tasks:
  - name: create_change_request
    task: servicenow_create_change
    args:
      short_description: "Automated backup"
      servicenow_config: "{{ servicenow_config }}"
```

### **5. Schedule Automated Runs**

**Using cron (Linux/macOS):**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/my-network-automation && nornflow run workflows/backup_devices.yaml
```

**Using systemd timer (Linux):**
```bash
# Create service file
sudo nano /etc/systemd/system/network-backup.service

[Unit]
Description=Network Device Backup

[Service]
Type=oneshot
WorkingDirectory=/path/to/my-network-automation
ExecStart=/usr/local/bin/nornflow run workflows/backup_devices.yaml

# Create timer file
sudo nano /etc/systemd/system/network-backup.timer

[Unit]
Description=Daily Network Backup

[Timer]
OnCalendar=daily
OnCalendar=02:00

[Install]
WantedBy=timers.target

# Enable and start
sudo systemctl enable network-backup.timer
sudo systemctl start network-backup.timer
```

**Using N8N scheduler:**
- Add a **"Schedule Trigger"** node in N8N
- Set to run daily at 2 AM
- Connect to **"Execute Command"** node
- Command: `nornflow run workflows/backup_devices.yaml`

---

## **🔧 Troubleshooting**

### **Issue: N8N won't start**

```bash
# Check if port 5678 is already in use
lsof -i :5678

# If in use, stop the process or use different port
docker run -d --name n8n -p 5679:5678 n8nio/n8n
```

### **Issue: Can't connect to devices**

```bash
# Test SSH connectivity manually
ssh username@192.168.1.10

# Check credentials
echo $DEVICE_USERNAME
echo $DEVICE_PASSWORD

# Test with NornFlow
nornflow run workflows/backup_devices.yaml --limit switch-01 --verbose
```

### **Issue: AI workflow generation fails**

```bash
# Check Anthropic API key
echo $ANTHROPIC_API_KEY

# Check N8N logs
docker logs n8n

# Verify API key in N8N:
# - Open workflow
# - Click AI Agent node
# - Check credentials
```

### **Issue: Tests fail**

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests with verbose output
pytest tests/ -vv

# Run specific test
pytest tests/test_backup_workflow.py::test_connectivity_check -vv
```

---

## **📚 Learn More**

### **Documentation:**
- [Complete Architecture Guide](N8N_AI_WORKFLOW_ARCHITECTURE.md) - How AI agents work
- [NornFlow Installation Guide](NORNFLOW_INSTALLATION_GUIDE.md) - Detailed setup
- [N8N Setup Guide](N8N_SETUP_COMPLETE_GUIDE.md) - N8N configuration
- [NornFlow NetOps Guide](NORNFLOW_NETOPS_COMPLETE_GUIDE.md) - Advanced features

### **Examples:**
- [Network Stack Generator](N8N_NETWORK_STACK_GENERATOR.md) - Form configuration
- [Sample Workflows](sample_workflows/) - More examples

### **Community:**
- GitHub Issues: Report bugs or request features
- Discussions: Ask questions, share workflows

---

## **💡 Pro Tips**

### **Tip 1: Use Variables for Credentials**

Never hardcode passwords! Use environment variables:

```yaml
# Good ✅
connection:
  username: "${DEVICE_USERNAME}"
  password: "${DEVICE_PASSWORD}"

# Bad ❌
connection:
  username: "admin"
  password: "password123"
```

### **Tip 2: Start with Dry Run**

Always test with `--dry-run` first:

```bash
# Safe - shows what would happen
nornflow run workflows/deploy_config.yaml --dry-run

# Then run for real
nornflow run workflows/deploy_config.yaml
```

### **Tip 3: Use Failure Strategies**

Choose the right strategy for your use case:

```yaml
# Skip failed devices, continue with others
failure_strategy: "skip-failed"  # ← Best for backups

# Stop on first failure
failure_strategy: "fail-fast"    # ← Best for deployments

# Run all, report failures at end
failure_strategy: "run-all"      # ← Best for discovery
```

### **Tip 4: Version Control Everything**

```bash
# Initialize Git in your project
cd my-network-automation
git init
git add .
git commit -m "Initial AI-generated network automation"

# Push to GitHub
git remote add origin https://github.com/yourname/my-network-automation.git
git push -u origin main
```

### **Tip 5: Monitor Your Workflows**

Add monitoring to every workflow:

```yaml
tasks:
  - name: push_metrics
    task: prometheus_push_metrics
    args:
      job_name: "network_backup"
      metrics:
        backup_success: "{{ 1 if backup_result.success else 0 }}"
        backup_duration: "{{ backup_result.duration }}"
```

---

## **🎉 Success!**

You now have:

✅ AI-powered workflow generator running  
✅ Your first network automation workflow  
✅ Complete test suite  
✅ Production-ready code  
✅ Knowledge to create more workflows  

**Time to automate your network!** 🚀

---

## **❓ Need Help?**

- **Documentation:** Check the guides in this repository
- **Issues:** [GitHub Issues](https://github.com/chasewoodard93/n8n-network-automation/issues)
- **Questions:** [GitHub Discussions](https://github.com/chasewoodard93/n8n-network-automation/discussions)

---

**Happy Automating!** 🎊

