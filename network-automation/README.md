# 🚀 AI-Powered Network Automation Platform

**Complete enterprise-grade network automation platform combining NornFlow NetOps, LabFlow, AI Learning Loop, and N8N orchestration.**

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![NornFlow](https://img.shields.io/badge/NornFlow-v0.4.0-green)](https://github.com/theandrelima/nornflow)

---

## **📋 Table of Contents**

- [Overview](#overview)
- [Platform Components](#platform-components)
- [Quick Start](#quick-start)
  - [For macOS Users](#for-macos-users)
  - [For Windows Users (WSL)](#for-windows-users-wsl)
  - [For Linux Users](#for-linux-users)
- [Installation Guides](#installation-guides)
- [Features](#features)
- [Use Cases](#use-cases)
- [Documentation](#documentation)
- [Architecture](#architecture)
- [Contributing](#contributing)

---

## **🎯 Overview**

This platform provides a **complete AI-powered network automation solution** that combines:

1. **NornFlow NetOps v0.4.0** - Enterprise network automation framework
2. **LabFlow** - Intelligent lab environment manager
3. **AI Learning Loop** - Self-improving automation with Claude AI
4. **N8N Orchestration** - Workflow automation and integration
5. **Network Stack Generator** - One-click project generation

### **What Makes This Special?**

✅ **AI-Powered** - Automatically learns from failures and improves  
✅ **Enterprise-Ready** - RBAC, secrets management, monitoring, CI/CD  
✅ **Multi-Platform** - Works on macOS, Windows (WSL), and Linux  
✅ **Highly Integrated** - NetBox, Git, ServiceNow, Jira, Grafana, Prometheus  
✅ **Production-Tested** - 93 tests with 100% coverage  
✅ **One-Click Setup** - Auto-generate complete projects via web form  

---

## **🏗️ Platform Components**

### **1. NornFlow NetOps (v0.4.0)**

Enterprise-grade network automation framework with custom enhancements.

**Official Features (v0.4.0):**
- Workflow orchestration with YAML
- Failure strategies (skip-failed, fail-fast, run-all)
- Meaningful exit codes (0-100 for failures)
- Python 3.13 support
- Enhanced CLI

**Custom Enhancements (8 Areas):**
- **Network Tasks** - Config, discovery, backup, compliance
- **Workflow Control** - Conditionals, loops, retry, dependencies
- **Integrations** - NetBox, Git, ServiceNow, Jira, Grafana, Prometheus
- **Testing** - 93 tests with 100% coverage
- **User Experience** - AWX, NetPicker, Web UI, Postman
- **Security** - RBAC, secrets management (Vault, AWS, Azure, Doppler)
- **Scheduling** - Cron, interval, one-time, event-driven
- **Visualization** - Real-time dashboards with D3.js

### **2. LabFlow**

Intelligent lab environment manager that automatically selects the best provider.

**Features:**
- ContainerLab for free virtual devices
- Terraform + Azure for licensed devices
- Smart provider selection
- Cost optimization
- Automatic cleanup

### **3. AI Learning Loop**

Self-improving automation powered by Claude AI.

**Features:**
- Automatic failure analysis
- Code generation and fixes
- Iterative improvement
- GitHub integration
- Slack notifications

### **4. N8N Network Stack Generator**

One-click generation of complete NornFlow projects.

**Features:**
- Web form for configuration
- Auto-generate inventory
- Pre-configured integrations
- Ready-to-use workflows
- CI/CD pipelines included

---

## **⚡ Quick Start**

Choose your platform:

### **For macOS Users**

#### **Prerequisites**

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Verify installation
python3.11 --version
```

#### **Install NornFlow NetOps**

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Clone repository
mkdir -p ~/projects
cd ~/projects
git clone --recurse-submodules https://github.com/YOUR_USERNAME/n8n.git
cd n8n/nornflow-netops

# Install dependencies
uv sync
uv pip install -e .

# Verify installation
nornflow --version  # Should show 0.4.0
```

#### **Install Network Automation Libraries**

```bash
# Core libraries
pip3 install nornir nornir-utils nornir-netmiko nornir-napalm

# Optional but recommended
pip3 install textfsm ntc-templates jinja2 pyyaml
```

#### **Create Your First Project**

```bash
# Create project directory
mkdir ~/projects/my-network-automation
cd ~/projects/my-network-automation

# Initialize NornFlow project
nornflow init

# Create additional directories
mkdir -p configs/backups logs documentation
```

---

### **For Windows Users (WSL)**

#### **Prerequisites**

```bash
# Update WSL
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Verify installation
python3.11 --version
```

#### **Install NornFlow NetOps**

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Clone repository
mkdir -p ~/projects
cd ~/projects
git clone --recurse-submodules https://github.com/YOUR_USERNAME/n8n.git
cd n8n/nornflow-netops

# Install dependencies
uv sync
uv pip install -e .

# Verify installation
nornflow --version  # Should show 0.4.0
```

#### **Install Network Automation Libraries**

```bash
# Core libraries
pip3 install nornir nornir-utils nornir-netmiko nornir-napalm

# Optional but recommended
pip3 install textfsm ntc-templates jinja2 pyyaml
```

#### **Create Your First Project**

```bash
# Create project directory
mkdir ~/projects/my-network-automation
cd ~/projects/my-network-automation

# Initialize NornFlow project
nornflow init

# Create additional directories
mkdir -p configs/backups logs documentation
```

---

### **For Linux Users**

#### **Prerequisites**

```bash
# Update system
sudo apt update && sudo apt upgrade -y  # Debian/Ubuntu
# OR
sudo yum update -y  # RHEL/CentOS

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y  # Debian/Ubuntu
# OR
sudo yum install python3.11 python3-pip git -y  # RHEL/CentOS

# Verify installation
python3.11 --version
```

#### **Install NornFlow NetOps**

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Clone repository
mkdir -p ~/projects
cd ~/projects
git clone --recurse-submodules https://github.com/YOUR_USERNAME/n8n.git
cd n8n/nornflow-netops

# Install dependencies
uv sync
uv pip install -e .

# Verify installation
nornflow --version  # Should show 0.4.0
```

#### **Install Network Automation Libraries**

```bash
# Core libraries
pip3 install nornir nornir-utils nornir-netmiko nornir-napalm

# Optional but recommended
pip3 install textfsm ntc-templates jinja2 pyyaml
```

#### **Create Your First Project**

```bash
# Create project directory
mkdir ~/projects/my-network-automation
cd ~/projects/my-network-automation

# Initialize NornFlow project
nornflow init

# Create additional directories
mkdir -p configs/backups logs documentation
```

---

## **🎯 Getting Started (Choose Your Path)**

### **Path 1: AI-Assisted Setup** (Recommended for beginners)
👉 **[CODEIUM_SETUP_PROMPT.md](CODEIUM_SETUP_PROMPT.md)**
- Copy prompt into Codeium, ChatGPT, or Copilot
- AI provides step-by-step guidance
- Get help with troubleshooting
- Time: ~45 minutes

### **Path 2: Self-Guided Setup** (Recommended for experienced users)
👉 **[GETTING_STARTED_DETAILED.md](GETTING_STARTED_DETAILED.md)**
- Follow 9 detailed steps with exact commands
- Platform-specific instructions (macOS, Windows, Linux)
- Built-in troubleshooting tips
- Time: ~45 minutes

### **Compare Both Approaches**
👉 **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)**
- Quick comparison table
- Decision guide
- Prerequisites checklist
- Success indicators

---

## **📚 Installation Guides**

Detailed platform-specific guides:

- **[macOS Installation Guide](NORNFLOW_INSTALLATION_GUIDE.md#for-macos-users)** - Complete setup for Mac users
- **[Windows/WSL Installation Guide](NORNFLOW_INSTALLATION_GUIDE.md#for-windows-users-wsl)** - Complete setup for Windows users
- **[Linux Installation Guide](NORNFLOW_INSTALLATION_GUIDE.md#for-linux-users)** - Complete setup for Linux users
- **[Complete Installation Guide](NORNFLOW_INSTALLATION_GUIDE.md)** - All platforms with examples

---

## **✨ Features**

### **Network Automation**
- ✅ Device configuration management (CLI + API)
- ✅ Template-based config with Jinja2
- ✅ Automated backups with versioning
- ✅ Compliance checking and reporting
- ✅ Network discovery (LLDP/CDP, interfaces, device info)
- ✅ Multi-platform support (Cisco IOS/NX-OS, Arista EOS, Juniper)

### **Workflow Orchestration**
- ✅ Conditional execution (when/unless)
- ✅ Loops and iteration (loop/with_items/until)
- ✅ Error handling (rescue/always blocks)
- ✅ Retry mechanisms with exponential backoff
- ✅ Task dependencies and parallel execution
- ✅ Failure strategies (skip-failed, fail-fast, run-all)

### **Enterprise Integrations**
- ✅ **NetBox** - IPAM, DCIM, config context (8 tasks)
- ✅ **Git** - Version control, drift detection (8 tasks)
- ✅ **ServiceNow** - Change management, CMDB (5 tasks)
- ✅ **Jira** - Issue tracking, project management (3 tasks)
- ✅ **Grafana** - Dashboards, alerts (3 tasks)
- ✅ **Prometheus** - Metrics collection (2 tasks)
- ✅ **Infoblox** - DNS/DHCP/IPAM (1 task)

### **User Interfaces**
- ✅ **CLI** - Command-line interface
- ✅ **Ansible AWX** - Job templates, surveys, RBAC
- ✅ **NetPicker** - Auto-generated web forms
- ✅ **Web Dashboard** - Real-time monitoring with D3.js
- ✅ **Postman** - API collection generation

### **Security & Compliance**
- ✅ **RBAC** - Role-based access control
- ✅ **Secrets Management** - Vault, AWS, Azure, Doppler, local encrypted
- ✅ **Audit Logging** - Complete audit trail
- ✅ **Security Middleware** - JWT, rate limiting, CORS

### **Scheduling & Orchestration**
- ✅ **Cron Scheduling** - Traditional cron with seconds precision
- ✅ **Interval Scheduling** - Run every X seconds/minutes/hours
- ✅ **One-time Scheduling** - Run once at specific time
- ✅ **Event-driven** - Webhooks, file changes, API triggers
- ✅ **Resource Management** - CPU, memory, network allocation

### **Monitoring & Visualization**
- ✅ **Real-time Dashboard** - D3.js workflow visualization
- ✅ **Performance Analytics** - Execution metrics, success rates
- ✅ **System Health** - Resource utilization, alerts
- ✅ **WebSocket Updates** - Live execution status

---

## **🎯 Use Cases**

### **Use Case 1: Automated Network Deployment**
Deploy VLANs to 100 switches with complete change management.

**Time:** 5 minutes (vs 2 hours manual)

**Workflow:**
1. Create ServiceNow change request
2. Get device list from NetBox
3. Backup all configs to Git
4. Silence Grafana alerts
5. Deploy VLAN configuration
6. Validate deployment
7. Push metrics to Prometheus
8. Update change request

### **Use Case 2: Compliance Auditing**
Check 500 devices for compliance violations.

**Time:** 10 minutes (vs 1 day manual)

**Workflow:**
1. Discover all devices from NetBox
2. Execute compliance checks
3. Generate compliance report
4. Create Jira issues for violations
5. Update Grafana dashboard

### **Use Case 3: Configuration Drift Detection**
Detect unauthorized changes across network.

**Time:** Continuous (scheduled every hour)

**Workflow:**
1. Backup current configs
2. Compare with Git repository
3. Detect drift
4. Create ServiceNow incident
5. Generate drift report
6. Alert via Slack

---

## **📖 Documentation**

### **Getting Started**
- [Complete Installation Guide](NORNFLOW_INSTALLATION_GUIDE.md) - All platforms
- [NornFlow NetOps Complete Guide](NORNFLOW_NETOPS_COMPLETE_GUIDE.md) - Tool overview
- [Quick Start Examples](#quick-start) - Platform-specific setup

### **Platform Components**
- [NornFlow NetOps Documentation](nornflow-netops/README.md) - Core framework
- [LabFlow Documentation](labflow-automation/README.md) - Lab management
- [AI Learning Loop](enhancements/AI_LEARNING_LOOP_SETUP.md) - AI integration

### **Advanced Topics**
- [N8N Stack Generator](N8N_NETWORK_STACK_GENERATOR.md) - Auto-generate projects
- [Network Tasks](enhancements/network_tasks/README.md) - Task library
- [Workflow Control](enhancements/workflow_control/README.md) - Advanced control
- [Integrations](enhancements/integrations/README.md) - External systems

### **Deployment**
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) - Production deployment
- [Upgrade Guide](EASY_UPGRADE_GUIDE.md) - Upgrading NornFlow

---

## **🏛️ Architecture**

### **System Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interfaces                          │
│  CLI │ AWX │ NetPicker │ Web Dashboard │ Postman │ N8N Form     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NornFlow Core v0.4.0                         │
│  Workflow Engine │ Task Catalog │ Variable System │ Failure     │
│  Strategies │ Exit Codes                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Custom Enhancements                           │
│  Network Tasks │ Workflow Control │ Integrations │ Security    │
│  Scheduling │ Visualization │ Testing                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  External   │  │   Network   │  │  LabFlow    │
│  Systems    │  │   Devices   │  │  Env Mgmt   │
│             │  │             │  │             │
│ • NetBox    │  │ • Cisco IOS │  │ • Container │
│ • Git       │  │ • NX-OS     │  │ • Terraform │
│ • ServiceNow│  │ • Arista    │  │ • Azure     │
│ • Jira      │  │ • Juniper   │  │             │
│ • Grafana   │  │             │  │             │
│ • Prometheus│  │             │  │             │
└─────────────┘  └─────────────┘  └─────────────┘
```

### **Component Interaction**

1. **User** submits workflow via CLI, AWX, Web UI, or N8N
2. **NornFlow Engine** parses workflow and validates
3. **Task Catalog** loads required tasks
4. **Workflow Control** applies conditionals, loops, retry logic
5. **Integrations** interact with external systems
6. **Network Tasks** execute on devices
7. **Results** collected and processed
8. **Monitoring** updates dashboards and metrics

---

## **📝 Example Workflows**

### **Example 1: Simple Backup**

```yaml
# workflows/backup_devices.yaml
---
workflow:
  name: "Backup Network Devices"
  description: "Backup configurations from all devices"

  vars:
    backup_dir: "configs/backups/{{ '%Y-%m-%d' | strftime }}"

  tasks:
    - name: test_connectivity
      task: test_connectivity
      args:
        method: ssh
        timeout: 10
      set_to: connectivity_result

    - name: backup_config
      task: backup_config
      args:
        backup_dir: "{{ backup_dir }}"
      when: "{{ connectivity_result.success }}"
```

**Run it:**
```bash
nornflow run workflows/backup_devices.yaml
```

---

### **Example 2: Configuration Deployment with Validation**

```yaml
# workflows/deploy_vlans.yaml
---
workflow:
  name: "Deploy VLAN Configuration"
  failure_strategy: "skip-failed"  # NEW in v0.4.0

  vars:
    vlans:
      - id: 10
        name: "DATA"
      - id: 20
        name: "VOICE"

  tasks:
    # Backup before changes
    - name: backup_config
      task: backup_config
      args:
        backup_dir: "configs/backups/pre-vlan-deploy"

    # Deploy VLAN configuration
    - name: deploy_config
      task: deploy_config
      args:
        template_file: "templates/{{ host.platform }}/vlans.j2"
        template_vars:
          vlans: "{{ vlans }}"
        backup_before: false
        validate_after: true
        rollback_on_error: true
      retry:
        max_attempts: 3
        delay: 5
```

**Run it:**
```bash
nornflow run workflows/deploy_vlans.yaml --groups switches
```

---

### **Example 3: Complete Change Management Workflow**

```yaml
# workflows/change_management.yaml
---
workflow:
  name: "Change Management with Full Integration"
  failure_strategy: "skip-failed"

  vars:
    servicenow_config:
      instance_url: "https://company.service-now.com"
      username: "${SERVICENOW_USER}"
      password: "${SERVICENOW_PASS}"

    netbox_config:
      url: "https://netbox.company.com"
      token: "${NETBOX_TOKEN}"

    git_config:
      repo_path: "/opt/network-configs"
      author_name: "NornFlow Automation"
      author_email: "nornflow@company.com"

  tasks:
    # 1. Create ServiceNow change request
    - name: servicenow_create_change
      task: servicenow_create_change
      args:
        short_description: "Network config update - {{ host.name }}"
        description: "Automated VLAN deployment"
        servicenow_config: "{{ servicenow_config }}"
      set_to: change_request

    # 2. Get device info from NetBox
    - name: netbox_get_device
      task: netbox_get_device
      args:
        device_name: "{{ host.name }}"
        netbox_config: "{{ netbox_config }}"
      set_to: netbox_device

    # 3. Backup to Git
    - name: backup_config
      task: backup_config
      set_to: backup_result

    - name: git_commit_config
      task: git_commit_config
      args:
        config_content: "{{ backup_result.config }}"
        device_name: "{{ host.name }}"
        commit_message: "Pre-change backup for CR {{ change_request.number }}"
        git_config: "{{ git_config }}"

    # 4. Deploy configuration
    - name: deploy_config
      task: deploy_config
      args:
        template_file: "templates/{{ host.platform }}/config.j2"
        template_vars: "{{ netbox_device.config_context }}"
        validate_after: true
        rollback_on_error: true
      retry:
        max_attempts: 3
        delay: 5
      set_to: deploy_result

    # 5. Update ServiceNow
    - name: servicenow_update_change
      task: servicenow_update_change
      args:
        change_number: "{{ change_request.number }}"
        state: "{{ 'completed' if deploy_result.success else 'failed' }}"
        servicenow_config: "{{ servicenow_config }}"

    # 6. Push metrics
    - name: prometheus_push_metrics
      task: prometheus_push_metrics
      args:
        job_name: "nornflow_change_management"
        metrics:
          deployment_success: "{{ 1 if deploy_result.success else 0 }}"
```

**Run it:**
```bash
nornflow run workflows/change_management.yaml
```

---

## **🚀 N8N Network Stack Generator**

Generate complete NornFlow projects with a web form!

### **Features**

- ✅ Web form for configuration
- ✅ Auto-generate complete project structure
- ✅ Pre-configured integrations
- ✅ Ready-to-use workflows
- ✅ CI/CD pipelines included
- ✅ Complete documentation

### **Setup**

```bash
# Install N8N
npm install n8n -g

# Or use Docker
docker run -it --rm -p 5678:5678 n8nio/n8n

# Import workflow
# 1. Open N8N at http://localhost:5678
# 2. Import n8n-workflows/network_stack_generator.json
# 3. Activate workflow
# 4. Access form URL
```

### **Usage**

1. Fill out the web form with your network details:
   - Network devices (switches, routers, firewalls)
   - Integration tools (NetBox, ServiceNow, Grafana)
   - CI/CD preferences (GitHub Actions, GitLab CI)
   - Workflow templates to generate

2. Submit the form

3. Download the generated project ZIP

4. Extract and start using:
   ```bash
   unzip my-network-automation.zip
   cd my-network-automation
   cp .env.example .env
   # Edit .env with your credentials
   nornflow run workflows/backup_devices.yaml
   ```

**See:** [N8N Stack Generator Guide](N8N_NETWORK_STACK_GENERATOR.md)

---

## **🔧 Configuration**

### **Inventory Setup**

**1. Define Devices (inventory/hosts.yaml)**

```yaml
---
switch-01:
  hostname: 192.168.1.10
  platform: ios
  groups:
    - switches
    - access
  data:
    site: datacenter-1
    role: access-switch

router-01:
  hostname: 192.168.1.1
  platform: ios
  groups:
    - routers
    - edge
  data:
    site: datacenter-1
    role: edge-router
```

**2. Define Groups (inventory/groups.yaml)**

```yaml
---
switches:
  data:
    device_type: switch
    backup_enabled: true

routers:
  data:
    device_type: router
    backup_enabled: true
```

**3. Set Defaults (inventory/defaults.yaml)**

```yaml
---
username: admin
password: ${NETWORK_PASSWORD}
platform: ios

connection_options:
  netmiko:
    extras:
      conn_timeout: 10
```

**4. Environment Variables (.env)**

```bash
# Network credentials
NETWORK_PASSWORD=YourPassword123

# Integration credentials
NETBOX_TOKEN=your-netbox-token
SERVICENOW_USER=your-snow-user
SERVICENOW_PASS=your-snow-pass
```

---

## **🧪 Testing**

### **Run Tests**

```bash
# Run all tests
cd nornflow-netops
pytest tests/

# Run specific test category
pytest tests/unit/
pytest enhancements/testing/

# Run with coverage
pytest --cov=nornflow --cov-report=html
```

### **Validate Workflows**

```bash
# Dry run (don't execute)
nornflow run workflows/backup_devices.yaml --dry-run

# Show what would be executed
nornflow show --workflows
nornflow show --tasks
nornflow show --hosts
```

---

## **📊 Monitoring**

### **Start Web Dashboard**

```bash
cd nornflow-netops
python -m enhancements.visualization.monitoring_dashboard

# Access at http://localhost:5000
```

**Features:**
- Real-time workflow visualization
- Execution status and progress
- Performance metrics
- System health monitoring
- WebSocket live updates

---

## **📚 Complete Documentation**

### **Getting Started**
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Choose your setup path (AI-assisted or self-guided)
- **[CODEIUM_SETUP_PROMPT.md](CODEIUM_SETUP_PROMPT.md)** - AI-assisted setup with Codeium/ChatGPT
- **[GETTING_STARTED_DETAILED.md](GETTING_STARTED_DETAILED.md)** - Step-by-step self-guided setup
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - 5-minute quick start

### **Installation & Setup**
- **[NORNFLOW_INSTALLATION_GUIDE.md](NORNFLOW_INSTALLATION_GUIDE.md)** - Platform-specific installation (macOS, Windows, Linux)
- **[N8N_SETUP_COMPLETE_GUIDE.md](N8N_SETUP_COMPLETE_GUIDE.md)** - Complete N8N setup with 3 installation options
- **[NORNFLOW_NETOPS_COMPLETE_GUIDE.md](NORNFLOW_NETOPS_COMPLETE_GUIDE.md)** - NornFlow features and capabilities

### **Architecture & Design**
- **[N8N_AI_WORKFLOW_ARCHITECTURE.md](N8N_AI_WORKFLOW_ARCHITECTURE.md)** - Complete technical architecture
  - How AI agents work together
  - Three-layer architecture (UI → AI → Execution)
  - Workflow generation process
  - Testing & validation methodology
  - Real workflow examples
  - Interactive flowcharts

### **Workflow Generation**
- **[N8N_NETWORK_STACK_GENERATOR.md](N8N_NETWORK_STACK_GENERATOR.md)** - Network stack generator documentation
  - Form configuration
  - Generated output structure
  - Integration setup

### **Project Status**
- **[NORNFLOW_VERSION_COMPARISON.md](NORNFLOW_VERSION_COMPARISON.md)** - Version comparison (v0.3.1 → v0.4.0)
- **[EASY_UPGRADE_GUIDE.md](EASY_UPGRADE_GUIDE.md)** - How to upgrade NornFlow
- **[UPGRADE_COMPLETE.md](UPGRADE_COMPLETE.md)** - Upgrade completion status

---

## **🤝 Contributing**

We welcome contributions! Please see:

- [Contributing Guide](nornflow-netops/CONTRIBUTING.md)
- [Enhancement Recommendations](enhancements/recommendations.md)

---

## **📄 License**

This project is licensed under the GPL 3.0 License - see the [LICENSE](nornflow-netops/LICENSE) file for details.

---

## **🙏 Acknowledgments**

- **NornFlow** - Built on top of the excellent [NornFlow](https://github.com/theandrelima/nornflow) framework
- **Nornir** - Powered by [Nornir](https://github.com/nornir-automation/nornir)
- **Community** - Thanks to all contributors and users

---

## **📞 Support**

- **Documentation:** See [Documentation](#documentation) section
- **Issues:** Open an issue on GitHub
- **Discussions:** Join our community discussions

---

## **🗺️ Roadmap**

### **Completed** ✅
- NornFlow v0.4.0 upgrade
- 8 custom enhancement areas
- 93 tests with 100% coverage
- N8N stack generator
- Complete documentation

### **In Progress** 🚧
- Additional integration providers
- Enhanced AI learning capabilities
- Multi-tenant support

### **Planned** 📋
- Cloud-native deployment
- Advanced analytics
- Mobile app

---

**Built with ❤️ for Network Engineers**

**Get started today and automate your network!** 🚀

