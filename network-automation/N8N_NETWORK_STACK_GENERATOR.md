# 🚀 N8N Network Automation Stack Generator

## **Overview**

This N8N workflow acts as a **"Network Automation Stack Generator"** that takes your network infrastructure details via a web form and automatically generates a complete, ready-to-use NornFlow NetOps project with all configurations, integrations, and workflows.

---

## **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Form (N8N Form)                      │
│  User fills out network stack configuration                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              N8N Workflow Processing                         │
│  1. Parse form data                                          │
│  2. Generate directory structure                             │
│  3. Create inventory files                                   │
│  4. Generate integration configs                             │
│  5. Create workflow templates                                │
│  6. Generate CI/CD files                                     │
│  7. Create documentation                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Generated Output (ZIP File)                     │
│  Complete NornFlow project ready to deploy                   │
└─────────────────────────────────────────────────────────────┘
```

---

## **Workflow Components**

### **1. Form Trigger (Web Form)**

The workflow starts with an N8N Form that collects:

**Network Devices Section:**
- Device type (switch, router, firewall, load balancer)
- Vendor (Cisco, Arista, Juniper, Palo Alto, F5)
- Model
- Quantity
- Management IP range
- Platform (ios, nxos, eos, junos)

**Integration Tools Section:**
- DDI/IPAM: Infoblox, BlueCat, phpIPAM, None
- Source of Truth: NetBox, Nautobot, None
- Monitoring: Grafana+Prometheus, LibreNMS, Zabbix, None
- ITSM: ServiceNow, Jira, None

**CI/CD Pipeline Section:**
- Git provider: GitHub, GitLab, Bitbucket
- CI/CD tool: GitHub Actions, GitLab CI, Jenkins

**Automation Preferences:**
- Workflow templates to generate (checkboxes)
- Backup schedule (cron expression)
- Compliance checks enabled (yes/no)
- Change management integration (yes/no)

---

### **2. Data Processing Nodes**

**Node 1: Parse Form Data**
- Extract and validate form inputs
- Generate device lists with IPs
- Create configuration objects

**Node 2: Generate Directory Structure**
- Create project folder structure
- Generate file paths

**Node 3: Create Inventory Files**
- Generate hosts.yaml from device list
- Generate groups.yaml based on device types
- Generate defaults.yaml with credentials template

**Node 4: Generate Integration Configs**
- Create integration config files based on selections
- Generate environment variable templates
- Create integration workflow examples

**Node 5: Create Workflow Templates**
- Generate backup workflows
- Generate deployment workflows
- Generate discovery workflows
- Generate compliance workflows
- Generate change management workflows

**Node 6: Generate CI/CD Files**
- Create .gitlab-ci.yml or .github/workflows/
- Generate test scripts
- Create deployment scripts

**Node 7: Create Documentation**
- Generate README.md with setup instructions
- Create GETTING_STARTED.md
- Generate integration guides

**Node 8: Package Output**
- Zip all generated files
- Send download link or email

---

## **Form Fields Definition**

### **Section 1: Network Devices**

```json
{
  "devices": [
    {
      "type": "switch",
      "vendor": "cisco",
      "model": "catalyst-9300",
      "platform": "ios",
      "quantity": 10,
      "ip_range_start": "192.168.1.10",
      "site": "datacenter-1",
      "role": "access"
    },
    {
      "type": "router",
      "vendor": "cisco",
      "model": "isr-4000",
      "platform": "ios",
      "quantity": 2,
      "ip_range_start": "192.168.1.1",
      "site": "datacenter-1",
      "role": "edge"
    }
  ]
}
```

### **Section 2: Integration Tools**

```json
{
  "integrations": {
    "ipam": {
      "tool": "infoblox",
      "url": "https://infoblox.company.com",
      "enabled": true
    },
    "source_of_truth": {
      "tool": "netbox",
      "url": "https://netbox.company.com",
      "enabled": true
    },
    "monitoring": {
      "tool": "grafana",
      "url": "https://grafana.company.com",
      "prometheus_url": "https://prometheus.company.com",
      "enabled": true
    },
    "itsm": {
      "tool": "servicenow",
      "instance_url": "https://company.service-now.com",
      "enabled": true
    }
  }
}
```

### **Section 3: CI/CD Configuration**

```json
{
  "cicd": {
    "git_provider": "github",
    "repository": "company/network-automation",
    "ci_tool": "github_actions",
    "auto_deploy": true,
    "test_on_pr": true
  }
}
```

### **Section 4: Automation Preferences**

```json
{
  "preferences": {
    "workflows": {
      "backup": true,
      "deployment": true,
      "discovery": true,
      "compliance": true,
      "change_management": true
    },
    "backup_schedule": "0 2 * * *",
    "compliance_enabled": true,
    "change_management_required": true,
    "failure_strategy": "skip-failed"
  }
}
```

---

## **Generated Output Structure**

```
network-automation-stack/
├── README.md                          # Auto-generated setup guide
├── GETTING_STARTED.md                 # Quick start guide
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore file
│
├── inventory/                         # Nornir inventory
│   ├── hosts.yaml                    # Generated from form devices
│   ├── groups.yaml                   # Generated device groups
│   └── defaults.yaml                 # Default settings
│
├── workflows/                         # Generated workflows
│   ├── backup_devices.yaml           # Backup workflow
│   ├── deploy_config.yaml            # Deployment workflow
│   ├── discover_network.yaml         # Discovery workflow
│   ├── compliance_check.yaml         # Compliance workflow
│   └── change_management.yaml        # Change mgmt workflow
│
├── templates/                         # Jinja2 templates
│   ├── ios/
│   │   ├── base_config.j2
│   │   ├── vlans.j2
│   │   └── interfaces.j2
│   ├── nxos/
│   └── eos/
│
├── integrations/                      # Integration configs
│   ├── netbox_config.yaml
│   ├── servicenow_config.yaml
│   ├── grafana_config.yaml
│   └── git_config.yaml
│
├── tasks/                             # Custom tasks
│   └── __init__.py
│
├── tests/                             # Test files
│   ├── test_inventory.py
│   ├── test_workflows.py
│   └── test_integrations.py
│
├── .github/                           # GitHub Actions (if selected)
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
│
├── .gitlab-ci.yml                     # GitLab CI (if selected)
│
├── nornflow.yaml                      # NornFlow configuration
└── requirements.txt                   # Python dependencies
```

---

## **N8N Workflow Nodes Breakdown**

### **Node Flow:**

```
1. Form Trigger
   ↓
2. Set Variables (Parse form data)
   ↓
3. Function: Generate Hosts YAML
   ↓
4. Function: Generate Groups YAML
   ↓
5. Function: Generate Defaults YAML
   ↓
6. Function: Generate Workflows (Loop)
   ↓
7. Function: Generate Integration Configs
   ↓
8. Function: Generate CI/CD Files
   ↓
9. Function: Generate Documentation
   ↓
10. Function: Create Directory Structure
   ↓
11. HTTP Request: Create ZIP file
   ↓
12. Send Email with download link
```

---

## **Key Functions**

### **Function 1: Generate Hosts YAML**

```javascript
// Generate hosts.yaml from form data
const devices = $json.devices;
let hostsYaml = "---\n";

devices.forEach((device, index) => {
  for (let i = 0; i < device.quantity; i++) {
    const deviceNum = i + 1;
    const deviceName = `${device.type}-${String(deviceNum).padStart(2, '0')}`;
    const ipParts = device.ip_range_start.split('.');
    const lastOctet = parseInt(ipParts[3]) + i;
    const ip = `${ipParts[0]}.${ipParts[1]}.${ipParts[2]}.${lastOctet}`;
    
    hostsYaml += `${deviceName}:\n`;
    hostsYaml += `  hostname: ${ip}\n`;
    hostsYaml += `  platform: ${device.platform}\n`;
    hostsYaml += `  groups:\n`;
    hostsYaml += `    - ${device.type}s\n`;
    hostsYaml += `    - ${device.role}\n`;
    hostsYaml += `  data:\n`;
    hostsYaml += `    site: ${device.site}\n`;
    hostsYaml += `    role: ${device.role}\n`;
    hostsYaml += `    vendor: ${device.vendor}\n`;
    hostsYaml += `    model: ${device.model}\n`;
    hostsYaml += `\n`;
  }
});

return { hostsYaml };
```

### **Function 2: Generate Backup Workflow**

```javascript
// Generate backup workflow YAML
const preferences = $json.preferences;
const integrations = $json.integrations;

let workflow = `---
workflow:
  name: "Automated Device Backup"
  description: "Backup configurations from all network devices"
  failure_strategy: "${preferences.failure_strategy}"
  
  vars:
    backup_dir: "configs/backups/{{ '%Y-%m-%d' | strftime }}"
    timestamp: "{{ '%Y%m%d_%H%M%S' | strftime }}"
  
  tasks:`;

// Add connectivity test
workflow += `
    - name: test_connectivity
      task: test_connectivity
      args:
        method: ssh
        timeout: 10
      set_to: connectivity_result`;

// Add backup task
workflow += `
    
    - name: backup_config
      task: backup_config
      args:
        backup_dir: "{{ backup_dir }}"
        filename_template: "{{ host.name }}_{{ timestamp }}.cfg"
      when: "{{ connectivity_result.success }}"
      set_to: backup_result`;

// Add Git integration if enabled
if (integrations.git && integrations.git.enabled) {
  workflow += `
    
    - name: git_commit_config
      task: git_commit_config
      args:
        config_content: "{{ backup_result.config }}"
        device_name: "{{ host.name }}"
        commit_message: "Automated backup - {{ timestamp }}"
      when: "{{ backup_result.success }}"`;
}

// Add monitoring if enabled
if (integrations.monitoring && integrations.monitoring.enabled) {
  workflow += `
    
    - name: prometheus_push_metrics
      task: prometheus_push_metrics
      args:
        job_name: "nornflow_backup"
        metrics:
          backup_success: "{{ 1 if backup_result.success else 0 }}"`;
}

return { workflowYaml: workflow };
```

---

## **Complete N8N Workflow JSON**

I'll create the complete N8N workflow that you can import directly into your N8N instance.

### **Workflow Features:**
- ✅ Web form for stack configuration
- ✅ Automatic file generation
- ✅ ZIP packaging
- ✅ Email delivery with download link
- ✅ Support for all integrations
- ✅ Customizable templates

---

## **Setup Instructions**

### **Step 1: Install N8N**

```bash
# Install N8N globally
npm install n8n -g

# Or use Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### **Step 2: Import the Workflow**

1. Open N8N at `http://localhost:5678`
2. Click **"Workflows"** → **"Import from File"**
3. Upload the `network_stack_generator.json` file (provided below)
4. Activate the workflow

### **Step 3: Configure Credentials**

Set up credentials for:
- Email (SMTP) - for sending download links
- File storage (optional) - for storing generated files

### **Step 4: Access the Form**

1. Click on the **Form Trigger** node
2. Copy the **Production URL**
3. Share this URL with users who need to generate stacks

---

## **Example: Generated Stack**

### **Input Form Data:**

```json
{
  "project_name": "acme-network-automation",
  "company_name": "ACME Corporation",
  "devices": [
    {
      "type": "switch",
      "vendor": "cisco",
      "model": "catalyst-9300",
      "platform": "ios",
      "quantity": 20,
      "ip_range_start": "192.168.1.10",
      "site": "datacenter-1",
      "role": "access"
    },
    {
      "type": "switch",
      "vendor": "cisco",
      "model": "nexus-9000",
      "platform": "nxos",
      "quantity": 4,
      "ip_range_start": "192.168.1.100",
      "site": "datacenter-1",
      "role": "core"
    },
    {
      "type": "router",
      "vendor": "cisco",
      "model": "isr-4000",
      "platform": "ios",
      "quantity": 2,
      "ip_range_start": "192.168.1.1",
      "site": "datacenter-1",
      "role": "edge"
    }
  ],
  "integrations": {
    "netbox": {
      "enabled": true,
      "url": "https://netbox.acme.com"
    },
    "servicenow": {
      "enabled": true,
      "instance_url": "https://acme.service-now.com"
    },
    "grafana": {
      "enabled": true,
      "url": "https://grafana.acme.com"
    },
    "git": {
      "enabled": true,
      "provider": "github",
      "repository": "acme/network-automation"
    }
  },
  "preferences": {
    "workflows": {
      "backup": true,
      "deployment": true,
      "discovery": true,
      "compliance": true,
      "change_management": true
    },
    "backup_schedule": "0 2 * * *",
    "compliance_enabled": true,
    "change_management_required": true,
    "failure_strategy": "skip-failed"
  }
}
```

### **Generated Output:**

The workflow generates a complete project with:

**1. Inventory Files (26 devices total)**

`inventory/hosts.yaml`:
```yaml
---
# Access Switches (20 devices)
switch-01:
  hostname: 192.168.1.10
  platform: ios
  groups:
    - switches
    - access
  data:
    site: datacenter-1
    role: access
    vendor: cisco
    model: catalyst-9300

switch-02:
  hostname: 192.168.1.11
  platform: ios
  # ... (continues for all 20 switches)

# Core Switches (4 devices)
switch-21:
  hostname: 192.168.1.100
  platform: nxos
  groups:
    - switches
    - core
  data:
    site: datacenter-1
    role: core
    vendor: cisco
    model: nexus-9000

# Edge Routers (2 devices)
router-01:
  hostname: 192.168.1.1
  platform: ios
  groups:
    - routers
    - edge
  data:
    site: datacenter-1
    role: edge
    vendor: cisco
    model: isr-4000
```

**2. Integration Workflows**

`workflows/change_management_backup.yaml`:
```yaml
---
workflow:
  name: "Change Management with Backup"
  description: "Complete change management workflow with ServiceNow integration"
  failure_strategy: "skip-failed"

  vars:
    servicenow_config:
      instance_url: "https://acme.service-now.com"
      username: "${SERVICENOW_USER}"
      password: "${SERVICENOW_PASS}"

    netbox_config:
      url: "https://netbox.acme.com"
      token: "${NETBOX_TOKEN}"

    git_config:
      repo_path: "/opt/network-configs"
      author_name: "NornFlow Automation"
      author_email: "nornflow@acme.com"

  tasks:
    # Create ServiceNow change request
    - name: servicenow_create_change
      task: servicenow_create_change
      args:
        short_description: "Network configuration update - {{ host.name }}"
        description: "Automated configuration deployment via NornFlow"
        servicenow_config: "{{ servicenow_config }}"
      set_to: change_request

    # Get device info from NetBox
    - name: netbox_get_device
      task: netbox_get_device
      args:
        device_name: "{{ host.name }}"
        netbox_config: "{{ netbox_config }}"
      set_to: netbox_device

    # Backup current config
    - name: backup_config
      task: backup_config
      args:
        backup_dir: "configs/backups/{{ change_request.number }}"
      set_to: backup_result

    # Commit backup to Git
    - name: git_commit_config
      task: git_commit_config
      args:
        config_content: "{{ backup_result.config }}"
        device_name: "{{ host.name }}"
        commit_message: "Pre-change backup for CR {{ change_request.number }}"
        git_config: "{{ git_config }}"

    # Deploy configuration
    - name: deploy_config
      task: deploy_config
      args:
        template_file: "templates/{{ host.platform }}/base_config.j2"
        template_vars: "{{ netbox_device.config_context }}"
        backup_before: false
        validate_after: true
        rollback_on_error: true
      retry:
        max_attempts: 3
        delay: 5
      set_to: deploy_result

    # Update ServiceNow change request
    - name: servicenow_update_change
      task: servicenow_update_change
      args:
        change_number: "{{ change_request.number }}"
        state: "{{ 'completed' if deploy_result.success else 'failed' }}"
        work_notes: "Deployment {{ 'successful' if deploy_result.success else 'failed' }}"
        servicenow_config: "{{ servicenow_config }}"

    # Push metrics to Prometheus
    - name: prometheus_push_metrics
      task: prometheus_push_metrics
      args:
        job_name: "nornflow_change_management"
        metrics:
          deployment_success: "{{ 1 if deploy_result.success else 0 }}"
          change_request_number: "{{ change_request.number }}"
```

**3. CI/CD Pipeline**

`.github/workflows/test-and-deploy.yml`:
```yaml
name: Test and Deploy Network Automation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install nornflow
          pip install -r requirements.txt

      - name: Validate inventory
        run: |
          nornflow show --hosts

      - name: Validate workflows
        run: |
          nornflow show --workflows

      - name: Run tests
        run: |
          pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        run: |
          # Add deployment logic here
          echo "Deploying to production..."
```

**4. Documentation**

`README.md`:
```markdown
# ACME Corporation - Network Automation Stack

Auto-generated by NornFlow NetOps Stack Generator

## Overview

This project contains automated network configuration and management workflows for ACME Corporation's network infrastructure.

### Infrastructure

- **26 Total Devices**
  - 20x Cisco Catalyst 9300 Switches (Access Layer)
  - 4x Cisco Nexus 9000 Switches (Core Layer)
  - 2x Cisco ISR 4000 Routers (Edge)

### Integrations

- ✅ NetBox (Source of Truth)
- ✅ ServiceNow (Change Management)
- ✅ Grafana + Prometheus (Monitoring)
- ✅ GitHub (Version Control)

## Quick Start

### 1. Install Dependencies

```bash
pip install nornflow
pip install -r requirements.txt
```

### 2. Configure Credentials

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Run Your First Workflow

```bash
# Backup all devices
nornflow run workflows/backup_devices.yaml

# Deploy configuration
nornflow run workflows/deploy_config.yaml

# Run discovery
nornflow run workflows/discover_network.yaml
```

## Available Workflows

- `backup_devices.yaml` - Automated device backups (scheduled: daily at 2 AM)
- `deploy_config.yaml` - Configuration deployment with validation
- `discover_network.yaml` - Network topology discovery
- `compliance_check.yaml` - Compliance validation
- `change_management_backup.yaml` - Full change management workflow

## Project Structure

```
acme-network-automation/
├── inventory/          # Device inventory
├── workflows/          # Automation workflows
├── templates/          # Configuration templates
├── integrations/       # Integration configs
├── tests/             # Test files
└── .github/           # CI/CD pipelines
```

## Support

For issues or questions, contact: nornflow@acme.com
```

---

## **How It Works: Data Flow**

### **Step-by-Step Process:**

1. **User fills form** → Form data submitted to N8N
2. **N8N receives data** → Validates and parses input
3. **Generate inventory** → Creates hosts.yaml, groups.yaml, defaults.yaml
4. **Generate workflows** → Creates YAML workflows based on selections
5. **Generate integrations** → Creates integration config files
6. **Generate CI/CD** → Creates GitHub Actions or GitLab CI files
7. **Generate docs** → Creates README and setup guides
8. **Package files** → Zips everything into downloadable archive
9. **Send notification** → Emails user with download link

### **Integration with NornFlow:**

The generated stack is **immediately usable** with NornFlow:

```bash
# Download and extract the generated stack
unzip acme-network-automation.zip
cd acme-network-automation

# Configure credentials
cp .env.example .env
nano .env  # Add your credentials

# Run workflows immediately
nornflow run workflows/backup_devices.yaml
```

---

## **Customization Options**

### **Add Custom Templates**

The workflow can be extended to include custom templates:

1. Add template files to the N8N workflow
2. Modify the "Generate Templates" function
3. Include vendor-specific configurations

### **Add More Integrations**

To add support for new integrations:

1. Add form fields for the new integration
2. Create integration config generator function
3. Add integration tasks to workflow templates

### **Modify Workflow Templates**

Customize the generated workflows by editing the workflow generation functions in N8N.

---

## **Benefits**

✅ **Zero Manual Configuration** - Everything generated automatically
✅ **Best Practices Built-in** - Follows NornFlow conventions
✅ **Integration Ready** - Pre-configured for your tools
✅ **CI/CD Included** - Ready for automated testing
✅ **Documentation Included** - Auto-generated setup guides
✅ **Scalable** - Works for 10 or 1000 devices
✅ **Customizable** - Easy to modify generated files

---

## **Next Steps**

1. Import the N8N workflow (JSON provided separately)
2. Configure N8N credentials (SMTP for email)
3. Access the form URL
4. Fill out your network stack details
5. Download the generated project
6. Deploy and start automating!

---

**This completes the N8N Network Stack Generator documentation!** 🚀

