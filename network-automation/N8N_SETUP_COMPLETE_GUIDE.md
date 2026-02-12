# 🚀 N8N Network Stack Generator: Complete Setup Guide

**Step-by-step guide to set up and use the N8N workflow for auto-generating NornFlow projects**

---

## **📋 Table of Contents**

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation Options](#installation-options)
4. [Step-by-Step Setup](#step-by-step-setup)
5. [Workflow Architecture](#workflow-architecture)
6. [Using the Workflow](#using-the-workflow)
7. [Understanding the Output](#understanding-the-output)
8. [Troubleshooting](#troubleshooting)

---

## **🎯 Overview**

The N8N Network Stack Generator is a workflow automation that:

1. **Presents a web form** where you input your network infrastructure details
2. **Processes the data** and generates a complete NornFlow project
3. **Creates all files** (inventory, workflows, integrations, CI/CD)
4. **Packages everything** into a downloadable ZIP file
5. **Sends you the download link** via email

**Time to set up:** 15-30 minutes  
**Time to generate a stack:** 2-5 minutes  
**Time saved per project:** 2-4 hours  

---

## **📦 Prerequisites**

### **System Requirements**

- **Node.js** 18.x or higher
- **npm** or **yarn**
- **2GB RAM** minimum
- **macOS, Windows, or Linux**

### **Optional (for production)**

- **PostgreSQL** or **MySQL** (for persistent storage)
- **SMTP server** (for email notifications)
- **Reverse proxy** (nginx/Apache for HTTPS)

---

## **🔧 Installation Options**

### **Option 1: Quick Start with npm (Recommended for Testing)**

**Best for:** Quick testing, local development

```bash
# Install N8N globally
npm install n8n -g

# Start N8N
n8n

# Access at http://localhost:5678
```

**Pros:**
- ✅ Fastest setup (2 minutes)
- ✅ No configuration needed
- ✅ Perfect for testing

**Cons:**
- ❌ Data stored in SQLite (not production-ready)
- ❌ Runs in foreground
- ❌ No persistence across restarts

---

### **Option 2: Docker (Recommended for Production)**

**Best for:** Production use, persistent data, easy management

```bash
# Create directory for N8N data
mkdir -p ~/.n8n

# Run N8N with Docker
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n

# Access at http://localhost:5678
```

**Pros:**
- ✅ Persistent data storage
- ✅ Runs in background
- ✅ Auto-restart on failure
- ✅ Easy to update

**Cons:**
- ❌ Requires Docker installed

---

### **Option 3: Docker Compose (Recommended for Production with Database)**

**Best for:** Production use with PostgreSQL, full features

**Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    restart: unless-stopped
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n_password
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U n8n']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: n8nio/n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n_password
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_secure_password
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  n8n_data:
```

**Start the stack:**

```bash
# Start N8N with PostgreSQL
docker-compose up -d

# Check logs
docker-compose logs -f n8n

# Access at http://localhost:5678
# Login: admin / your_secure_password
```

**Pros:**
- ✅ Production-ready
- ✅ PostgreSQL database
- ✅ Persistent data
- ✅ Authentication enabled
- ✅ Auto-restart

**Cons:**
- ❌ More complex setup

---

## **📝 Step-by-Step Setup**

### **Step 1: Install N8N**

Choose one of the installation options above. For this guide, we'll use **Docker** (Option 2).

```bash
# Create data directory
mkdir -p ~/.n8n

# Run N8N
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n

# Verify it's running
docker ps | grep n8n

# Check logs
docker logs n8n
```

**Expected output:**
```
Editor is now accessible via:
http://localhost:5678/
```

---

### **Step 2: Access N8N**

1. Open your browser
2. Navigate to `http://localhost:5678`
3. Create your account (first time only):
   - Email: your@email.com
   - Password: (choose a secure password)

---

### **Step 3: Import the Workflow**

Now we need to create the complete workflow. Let me first create the full workflow JSON file:

---

## **🔄 Workflow Architecture**

### **High-Level Flow**

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Form Trigger                                       │
│  - User fills web form with network details                 │
│  - Submits configuration                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Parse Form Data                                    │
│  - Extract device information                               │
│  - Extract integration settings                             │
│  - Extract workflow preferences                             │
│  - Validate inputs                                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Generate Inventory Files                           │
│  - Generate hosts.yaml (from device list)                   │
│  - Generate groups.yaml (device groups)                     │
│  - Generate defaults.yaml (credentials template)            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Generate Workflow Files                            │
│  - Generate backup workflow (if selected)                   │
│  - Generate deployment workflow (if selected)               │
│  - Generate discovery workflow (if selected)                │
│  - Generate compliance workflow (if selected)               │
│  - Generate change management workflow (if selected)        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Generate Integration Configs                       │
│  - Generate NetBox config (if enabled)                      │
│  - Generate ServiceNow config (if enabled)                  │
│  - Generate Grafana config (if enabled)                     │
│  - Generate Git config (if enabled)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Generate CI/CD Files                               │
│  - Generate GitHub Actions workflow (if GitHub selected)    │
│  - Generate GitLab CI config (if GitLab selected)           │
│  - Generate test scripts                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: Generate Documentation                             │
│  - Generate README.md with setup instructions               │
│  - Generate GETTING_STARTED.md                              │
│  - Generate integration guides                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 8: Create Directory Structure                         │
│  - Create project folder structure                          │
│  - Organize all generated files                             │
│  - Create .env.example                                      │
│  - Create .gitignore                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 9: Package Files                                      │
│  - Create ZIP archive                                       │
│  - Include all generated files                              │
│  - Name: {project_name}-{timestamp}.zip                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 10: Send Notification                                 │
│  - Email user with download link                            │
│  - Include project summary                                  │
│  - Include next steps                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER DOWNLOADS                           │
│  - User receives email                                      │
│  - Downloads ZIP file                                       │
│  - Extracts and uses project                                │
└─────────────────────────────────────────────────────────────┘
```

---

## **🔍 Detailed Node Flow**

### **Node-by-Node Breakdown**

```
[1] Form Trigger
    ↓
[2] Set Variables (Parse Form Data)
    ↓
[3] Function: Generate Hosts YAML
    ↓
[4] Function: Generate Groups YAML
    ↓
[5] Function: Generate Defaults YAML
    ↓
[6] IF: Backup Workflow Selected?
    ├─ YES → [7] Function: Generate Backup Workflow
    └─ NO  → Skip
    ↓
[8] IF: Deployment Workflow Selected?
    ├─ YES → [9] Function: Generate Deployment Workflow
    └─ NO  → Skip
    ↓
[10] IF: Discovery Workflow Selected?
    ├─ YES → [11] Function: Generate Discovery Workflow
    └─ NO  → Skip
    ↓
[12] IF: Compliance Workflow Selected?
    ├─ YES → [13] Function: Generate Compliance Workflow
    └─ NO  → Skip
    ↓
[14] IF: Change Management Workflow Selected?
    ├─ YES → [15] Function: Generate Change Management Workflow
    └─ NO  → Skip
    ↓
[16] IF: NetBox Enabled?
    ├─ YES → [17] Function: Generate NetBox Config
    └─ NO  → Skip
    ↓
[18] IF: ServiceNow Enabled?
    ├─ YES → [19] Function: Generate ServiceNow Config
    └─ NO  → Skip
    ↓
[20] IF: Grafana Enabled?
    ├─ YES → [21] Function: Generate Grafana Config
    └─ NO  → Skip
    ↓
[22] Function: Generate Git Config
    ↓
[23] IF: Git Provider = GitHub?
    ├─ YES → [24] Function: Generate GitHub Actions
    └─ NO  → [25] Function: Generate GitLab CI
    ↓
[26] Function: Generate README
    ↓
[27] Function: Generate GETTING_STARTED
    ↓
[28] Function: Generate .env.example
    ↓
[29] Function: Generate .gitignore
    ↓
[30] Function: Generate nornflow.yaml
    ↓
[31] Function: Create Directory Structure JSON
    ↓
[32] Function: Create ZIP Archive
    ↓
[33] Send Email with Download Link
    ↓
[34] Response: Success Message
```

---

## **📊 Data Flow Diagram**

```
USER INPUT (Form)
    │
    ├─ Project Name ────────────────────┐
    ├─ Company Name ────────────────────┤
    ├─ Devices (JSON) ──────────────────┤
    │   ├─ Type (switch/router/etc)     │
    │   ├─ Vendor (cisco/arista/etc)    │
    │   ├─ Model                         │
    │   ├─ Platform (ios/nxos/eos)      │
    │   ├─ Quantity                      │
    │   ├─ IP Range Start                │
    │   ├─ Site                          │
    │   └─ Role                          │
    ├─ NetBox Enabled (Yes/No) ─────────┤
    ├─ NetBox URL ──────────────────────┤
    ├─ ServiceNow Enabled (Yes/No) ─────┤
    ├─ ServiceNow URL ──────────────────┤
    ├─ Grafana Enabled (Yes/No) ────────┤
    ├─ Grafana URL ─────────────────────┤
    ├─ Git Provider (GitHub/GitLab) ────┤
    ├─ Git Repository ──────────────────┤
    ├─ Workflows to Generate ───────────┤
    │   ├─ Backup                        │
    │   ├─ Deployment                    │
    │   ├─ Discovery                     │
    │   ├─ Compliance                    │
    │   └─ Change Management             │
    ├─ Backup Schedule (Cron) ──────────┤
    ├─ Failure Strategy ────────────────┤
    └─ Email ───────────────────────────┤
                                        │
                                        ▼
                            PROCESSING ENGINE
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
            INVENTORY FILES      WORKFLOW FILES    INTEGRATION FILES
                    │                   │                   │
                    ├─ hosts.yaml       ├─ backup.yaml     ├─ netbox_config.yaml
                    ├─ groups.yaml      ├─ deploy.yaml     ├─ servicenow_config.yaml
                    └─ defaults.yaml    ├─ discover.yaml   ├─ grafana_config.yaml
                                        ├─ compliance.yaml └─ git_config.yaml
                                        └─ change_mgmt.yaml
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
              CI/CD FILES         DOCUMENTATION        CONFIG FILES
                    │                   │                   │
                    ├─ .github/         ├─ README.md        ├─ nornflow.yaml
                    │  └─ workflows/    ├─ GETTING_         ├─ .env.example
                    │     └─ test.yml   │  STARTED.md       └─ .gitignore
                    └─ .gitlab-ci.yml   └─ integration/
                                           guides/
                                        │
                                        ▼
                                  ZIP ARCHIVE
                                        │
                                        ▼
                                EMAIL TO USER
```

---

## **🎨 Creating the Workflow in N8N**

### **Step 3: Import the Workflow JSON**

1. **Open N8N** at `http://localhost:5678`

2. **Click "Workflows" in the left sidebar**

3. **Click "Add Workflow" (+ button)**

4. **Click the three dots (⋮) in the top right**

5. **Select "Import from File"**

6. **Navigate to and select:** `n8n-workflows/network_stack_generator.json`

7. **Click "Import"**

The workflow will be imported with all nodes configured!

---

### **Step 4: Configure the Workflow**

#### **4.1: Configure Form Trigger**

1. **Click on the "Form Trigger" node** (first node)

2. **Configure form fields:**
   - Form Title: "Network Automation Stack Generator"
   - Form Description: "Generate a complete NornFlow project tailored to your infrastructure"

3. **The form fields are already configured in the JSON:**
   - Project Name (text)
   - Company Name (text)
   - Devices (textarea - JSON format)
   - NetBox Settings (checkbox + URL)
   - ServiceNow Settings (checkbox + URL)
   - Grafana Settings (checkbox + URL)
   - Git Settings (dropdown + URL)
   - Workflows to Generate (multi-select)
   - Backup Schedule (text - cron format)
   - Failure Strategy (dropdown)
   - Email (email)

4. **Click "Save"**

---

#### **4.2: Test the Form**

1. **Click "Execute Workflow" button** (top right)

2. **Click "Test URL"** to get the form URL

3. **Copy the URL** (looks like: `http://localhost:5678/form/abc123`)

4. **Open in new tab** to see your form

---

### **Step 5: Activate the Workflow**

1. **Toggle the "Active" switch** in the top right (should turn green)

2. **The workflow is now live!**

3. **Share the form URL** with your team or bookmark it

---

## **📝 Using the Workflow**

### **Example: Creating a Network Stack**

Let's walk through creating a complete network automation stack for a data center.

#### **Step 1: Access the Form**

Open the form URL in your browser: `http://localhost:5678/form/YOUR_FORM_ID`

---

#### **Step 2: Fill Out the Form**

**Project Information:**
```
Project Name: datacenter-automation
Company Name: Acme Corporation
```

**Network Devices (JSON format):**
```json
[
  {
    "type": "switch",
    "vendor": "cisco",
    "model": "Catalyst 9300",
    "platform": "ios",
    "quantity": 10,
    "ip_range_start": "192.168.1.10",
    "site": "datacenter-1",
    "role": "access"
  },
  {
    "type": "switch",
    "vendor": "cisco",
    "model": "Nexus 9000",
    "platform": "nxos",
    "quantity": 4,
    "ip_range_start": "192.168.1.1",
    "site": "datacenter-1",
    "role": "core"
  },
  {
    "type": "router",
    "vendor": "cisco",
    "model": "ASR 1000",
    "platform": "ios",
    "quantity": 2,
    "ip_range_start": "192.168.1.254",
    "site": "datacenter-1",
    "role": "edge"
  },
  {
    "type": "firewall",
    "vendor": "cisco",
    "model": "ASA 5500",
    "platform": "asa",
    "quantity": 2,
    "ip_range_start": "192.168.1.250",
    "site": "datacenter-1",
    "role": "security"
  }
]
```

**Integrations:**
```
☑ Enable NetBox
  NetBox URL: https://netbox.acme.com

☑ Enable ServiceNow
  ServiceNow URL: https://acme.service-now.com

☑ Enable Grafana
  Grafana URL: https://grafana.acme.com

Git Provider: GitHub
Git Repository: https://github.com/acme/network-configs
```

**Workflows to Generate:**
```
☑ Backup Devices
☑ Deploy Configuration
☑ Network Discovery
☑ Compliance Check
☑ Change Management
```

**Advanced Settings:**
```
Backup Schedule: 0 2 * * *  (Daily at 2 AM)
Failure Strategy: skip-failed
Email: netops@acme.com
```

---

#### **Step 3: Submit the Form**

1. **Review all fields**
2. **Click "Submit"**
3. **Wait for processing** (2-5 minutes)

---

#### **Step 4: Receive Email Notification**

You'll receive an email with:

```
Subject: Your Network Automation Stack is Ready!

Hi there,

Your network automation stack "datacenter-automation" has been generated successfully!

Project Summary:
- 18 network devices configured
- 5 workflows generated
- 3 integrations configured
- CI/CD pipeline included

Download your stack:
http://localhost:5678/files/datacenter-automation-20250125-143022.zip

Next Steps:
1. Download and extract the ZIP file
2. Review the README.md for setup instructions
3. Configure credentials in .env file
4. Run your first workflow!

Happy automating!
```

---

#### **Step 5: Download and Extract**

```bash
# Download the ZIP (or click the link in email)
curl -O http://localhost:5678/files/datacenter-automation-20250125-143022.zip

# Extract
unzip datacenter-automation-20250125-143022.zip

# Navigate to project
cd datacenter-automation
```

---

## **📂 Understanding the Generated Output**

### **Directory Structure**

```
datacenter-automation/
├── README.md                          # Setup instructions
├── GETTING_STARTED.md                 # Quick start guide
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
├── nornflow.yaml                      # NornFlow configuration
│
├── inventory/                         # Device inventory
│   ├── hosts.yaml                     # 18 devices configured
│   ├── groups.yaml                    # Device groups (switches, routers, etc)
│   └── defaults.yaml                  # Default credentials
│
├── workflows/                         # Generated workflows
│   ├── backup_devices.yaml            # Daily backup workflow
│   ├── deploy_config.yaml             # Configuration deployment
│   ├── network_discovery.yaml         # Network discovery
│   ├── compliance_check.yaml          # Compliance checking
│   └── change_management.yaml         # Full change management
│
├── integrations/                      # Integration configs
│   ├── netbox_config.yaml             # NetBox integration
│   ├── servicenow_config.yaml         # ServiceNow integration
│   ├── grafana_config.yaml            # Grafana integration
│   └── git_config.yaml                # Git integration
│
├── templates/                         # Jinja2 templates
│   ├── ios/                           # Cisco IOS templates
│   │   ├── base_config.j2
│   │   ├── vlans.j2
│   │   └── interfaces.j2
│   ├── nxos/                          # Cisco NX-OS templates
│   │   ├── base_config.j2
│   │   └── vlans.j2
│   └── asa/                           # Cisco ASA templates
│       └── base_config.j2
│
├── configs/                           # Configuration storage
│   ├── backups/                       # Backup storage
│   └── generated/                     # Generated configs
│
├── logs/                              # Log files
│   └── .gitkeep
│
├── tests/                             # Test files
│   ├── test_inventory.py              # Inventory tests
│   ├── test_workflows.py              # Workflow tests
│   └── test_integrations.py           # Integration tests
│
├── .github/                           # GitHub Actions (if GitHub selected)
│   └── workflows/
│       ├── test.yml                   # Run tests on push
│       └── deploy.yml                 # Deploy on release
│
└── documentation/                     # Additional docs
    ├── integration_guides/
    │   ├── netbox_setup.md
    │   ├── servicenow_setup.md
    │   └── grafana_setup.md
    └── workflow_guides/
        ├── backup_guide.md
        ├── deployment_guide.md
        └── compliance_guide.md
```

---

### **Generated Files Explained**

#### **1. inventory/hosts.yaml**

```yaml
---
# Auto-generated by N8N Network Stack Generator
# Project: datacenter-automation
# Generated: 2025-01-25 14:30:22

# Access Switches (Cisco Catalyst 9300)
switch-access-01:
  hostname: 192.168.1.10
  platform: ios
  groups:
    - switches
    - access
    - cisco
  data:
    site: datacenter-1
    role: access
    vendor: cisco
    model: "Catalyst 9300"

switch-access-02:
  hostname: 192.168.1.11
  platform: ios
  groups:
    - switches
    - access
    - cisco
  data:
    site: datacenter-1
    role: access
    vendor: cisco
    model: "Catalyst 9300"

# ... (8 more access switches)

# Core Switches (Cisco Nexus 9000)
switch-core-01:
  hostname: 192.168.1.1
  platform: nxos
  groups:
    - switches
    - core
    - cisco
  data:
    site: datacenter-1
    role: core
    vendor: cisco
    model: "Nexus 9000"

# ... (3 more core switches)

# Edge Routers (Cisco ASR 1000)
router-edge-01:
  hostname: 192.168.1.254
  platform: ios
  groups:
    - routers
    - edge
    - cisco
  data:
    site: datacenter-1
    role: edge
    vendor: cisco
    model: "ASR 1000"

# ... (1 more edge router)

# Firewalls (Cisco ASA 5500)
firewall-01:
  hostname: 192.168.1.250
  platform: asa
  groups:
    - firewalls
    - security
    - cisco
  data:
    site: datacenter-1
    role: security
    vendor: cisco
    model: "ASA 5500"

# ... (1 more firewall)
```

---

#### **2. workflows/backup_devices.yaml**

```yaml
---
# Auto-generated Backup Workflow
# Schedule: Daily at 2 AM (0 2 * * *)

workflow:
  name: "Backup Network Devices"
  description: "Automated daily backup of all network devices"
  failure_strategy: "skip-failed"

  vars:
    backup_dir: "configs/backups/{{ '%Y-%m-%d' | strftime }}"
    git_repo: "https://github.com/acme/network-configs"
    git_branch: "main"

  tasks:
    # Test connectivity first
    - name: test_connectivity
      task: test_connectivity
      args:
        method: ssh
        timeout: 10
      set_to: connectivity_result

    # Backup configuration
    - name: backup_config
      task: backup_config
      args:
        backup_dir: "{{ backup_dir }}"
      when: "{{ connectivity_result.success }}"
      set_to: backup_result

    # Commit to Git
    - name: git_commit_backup
      task: git_commit_config
      args:
        config_content: "{{ backup_result.config }}"
        device_name: "{{ host.name }}"
        commit_message: "Automated backup - {{ '%Y-%m-%d %H:%M:%S' | strftime }}"
        git_config:
          repo_path: "{{ git_repo }}"
          branch: "{{ git_branch }}"
          author_name: "NornFlow Automation"
          author_email: "nornflow@acme.com"
      when: "{{ backup_result.success }}"

    # Push metrics to Prometheus
    - name: prometheus_push_metrics
      task: prometheus_push_metrics
      args:
        job_name: "nornflow_backup"
        metrics:
          backup_success: "{{ 1 if backup_result.success else 0 }}"
          backup_duration: "{{ backup_result.duration }}"
```

---

#### **3. workflows/change_management.yaml**

```yaml
---
# Auto-generated Change Management Workflow
# Integrates with ServiceNow, NetBox, Git, Grafana

workflow:
  name: "Change Management Workflow"
  description: "Complete change management with all integrations"
  failure_strategy: "skip-failed"

  vars:
    servicenow_config:
      instance_url: "https://acme.service-now.com"
      username: "${SERVICENOW_USER}"
      password: "${SERVICENOW_PASS}"

    netbox_config:
      url: "https://netbox.acme.com"
      token: "${NETBOX_TOKEN}"

    grafana_config:
      url: "https://grafana.acme.com"
      api_key: "${GRAFANA_API_KEY}"

    git_config:
      repo_path: "https://github.com/acme/network-configs"
      author_name: "NornFlow Automation"
      author_email: "nornflow@acme.com"

  tasks:
    # 1. Create ServiceNow change request
    - name: servicenow_create_change
      task: servicenow_create_change
      args:
        short_description: "Network config update - {{ host.name }}"
        description: "Automated configuration deployment via NornFlow"
        servicenow_config: "{{ servicenow_config }}"
      set_to: change_request

    # 2. Get device info from NetBox
    - name: netbox_get_device
      task: netbox_get_device
      args:
        device_name: "{{ host.name }}"
        netbox_config: "{{ netbox_config }}"
      set_to: netbox_device

    # 3. Silence Grafana alerts
    - name: grafana_silence_alerts
      task: grafana_create_silence
      args:
        duration: "1h"
        comment: "Change {{ change_request.number }} in progress"
        grafana_config: "{{ grafana_config }}"
      set_to: silence_result

    # 4. Backup current config
    - name: backup_config
      task: backup_config
      set_to: backup_result

    # 5. Commit backup to Git
    - name: git_commit_backup
      task: git_commit_config
      args:
        config_content: "{{ backup_result.config }}"
        device_name: "{{ host.name }}"
        commit_message: "Pre-change backup for CR {{ change_request.number }}"
        git_config: "{{ git_config }}"

    # 6. Deploy new configuration
    - name: deploy_config
      task: deploy_config
      args:
        template_file: "templates/{{ host.platform }}/base_config.j2"
        template_vars: "{{ netbox_device.config_context }}"
        validate_after: true
        rollback_on_error: true
      retry:
        max_attempts: 3
        delay: 5
      set_to: deploy_result

    # 7. Update ServiceNow change
    - name: servicenow_update_change
      task: servicenow_update_change
      args:
        change_number: "{{ change_request.number }}"
        state: "{{ 'completed' if deploy_result.success else 'failed' }}"
        work_notes: "Deployment {{ 'successful' if deploy_result.success else 'failed' }}"
        servicenow_config: "{{ servicenow_config }}"

    # 8. Remove Grafana silence
    - name: grafana_remove_silence
      task: grafana_delete_silence
      args:
        silence_id: "{{ silence_result.id }}"
        grafana_config: "{{ grafana_config }}"
```

---

## **🚀 Next Steps After Generation**

### **Step 1: Configure Credentials**

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

**Edit `.env`:**
```bash
# Network Device Credentials
NETWORK_USERNAME=admin
NETWORK_PASSWORD=YourSecurePassword123

# NetBox
NETBOX_TOKEN=your-netbox-api-token

# ServiceNow
SERVICENOW_USER=your-snow-user
SERVICENOW_PASS=your-snow-password

# Grafana
GRAFANA_API_KEY=your-grafana-api-key

# Git
GIT_USERNAME=your-git-username
GIT_TOKEN=your-git-token
```

---

### **Step 2: Test Connectivity**

```bash
# Test a single device
nornflow run workflows/backup_devices.yaml --hosts switch-access-01 --dry-run

# Test all devices
nornflow show --hosts
```

---

### **Step 3: Run Your First Workflow**

```bash
# Run backup workflow
nornflow run workflows/backup_devices.yaml

# Check results
ls -la configs/backups/$(date +%Y-%m-%d)/
```

---

### **Step 4: Set Up Scheduling**

```bash
# Add to crontab
crontab -e

# Add this line for daily backups at 2 AM
0 2 * * * cd /path/to/datacenter-automation && nornflow run workflows/backup_devices.yaml
```

---

## **🔧 Troubleshooting**

### **N8N Issues**

**1. N8N won't start**
```bash
# Check if port 5678 is in use
lsof -i :5678

# Kill existing process
kill -9 <PID>

# Restart N8N
docker restart n8n
```

**2. Form not accessible**
```bash
# Check N8N logs
docker logs n8n

# Verify workflow is active
# Go to N8N UI → Workflows → Check "Active" toggle
```

**3. Workflow execution fails**
```bash
# Check execution logs in N8N UI
# Click on workflow → Executions tab → View failed execution

# Common issues:
# - Missing form fields
# - Invalid JSON in devices field
# - Email configuration not set up
```

---

### **Generated Project Issues**

**1. Inventory file errors**
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('inventory/hosts.yaml'))"

# Check for duplicate hosts
grep "^[a-z]" inventory/hosts.yaml | sort | uniq -d
```

**2. Workflow validation errors**
```bash
# Validate workflow syntax
nornflow validate workflows/backup_devices.yaml

# Dry run to test
nornflow run workflows/backup_devices.yaml --dry-run
```

**3. Integration connection errors**
```bash
# Test NetBox connection
curl -H "Authorization: Token $NETBOX_TOKEN" https://netbox.acme.com/api/

# Test ServiceNow connection
curl -u "$SERVICENOW_USER:$SERVICENOW_PASS" https://acme.service-now.com/api/now/table/sys_user?sysparm_limit=1
```

---

## **📊 Workflow Execution Monitoring**

### **In N8N UI**

1. **Go to "Executions" tab**
2. **View all workflow runs**
3. **Click on execution to see:**
   - Input data
   - Each node's output
   - Execution time
   - Success/failure status

### **Example Execution Timeline**

```
[14:30:22] Form submitted
[14:30:23] Parsing form data... ✓
[14:30:24] Generating hosts.yaml... ✓
[14:30:25] Generating groups.yaml... ✓
[14:30:26] Generating defaults.yaml... ✓
[14:30:27] Generating backup workflow... ✓
[14:30:28] Generating deployment workflow... ✓
[14:30:29] Generating discovery workflow... ✓
[14:30:30] Generating compliance workflow... ✓
[14:30:31] Generating change management workflow... ✓
[14:30:32] Generating NetBox config... ✓
[14:30:33] Generating ServiceNow config... ✓
[14:30:34] Generating Grafana config... ✓
[14:30:35] Generating Git config... ✓
[14:30:36] Generating GitHub Actions... ✓
[14:30:37] Generating README... ✓
[14:30:38] Generating GETTING_STARTED... ✓
[14:30:39] Creating directory structure... ✓
[14:30:40] Creating ZIP archive... ✓
[14:30:41] Sending email... ✓
[14:30:42] Complete! ✓

Total time: 20 seconds
```

---

## **🎉 Summary**

You now have:

✅ **N8N installed and running**
✅ **Network Stack Generator workflow imported**
✅ **Web form accessible to users**
✅ **Complete understanding of the flow**
✅ **Example project generated**
✅ **Ready to automate network operations**

---

**Next Steps:**

1. **Share the form URL** with your team
2. **Generate your first real project**
3. **Customize the workflow** for your needs
4. **Set up production N8N** with PostgreSQL
5. **Configure email notifications**

**Happy automating!** 🚀

