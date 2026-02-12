# 📘 NornFlow NetOps: Complete Installation & Usage Guide

**Multi-Platform Guide for macOS, Windows (WSL), and Linux**

## **Table of Contents**

1. [Prerequisites & Dependencies](#prerequisites--dependencies)
   - [For macOS Users](#for-macos-users)
   - [For Windows Users (WSL)](#for-windows-users-wsl)
   - [For Linux Users](#for-linux-users)
2. [Installation](#installation)
3. [Project Initialization](#project-initialization)
4. [Inventory Configuration](#inventory-configuration)
5. [Creating Workflows](#creating-workflows)
6. [Running Workflows](#running-workflows)
7. [Using Custom Enhancements](#using-custom-enhancements)
8. [Troubleshooting](#troubleshooting)

---

## **Prerequisites & Dependencies**

### **System Requirements (All Platforms)**

- Python 3.10, 3.11, 3.12, or 3.13
- Git
- 2GB RAM minimum (4GB+ recommended)
- Network connectivity to target devices

---

### **For macOS Users**

#### **Step 1: Install Homebrew (if not already installed)**

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify installation
brew --version
```

#### **Step 2: Install Python 3.11**

```bash
# Install Python 3.11
brew install python@3.11

# Verify installation
python3.11 --version  # Should show 3.11.x

# Install Git (if not already installed)
brew install git
git --version
```

#### **Step 3: Install uv (Modern Python Package Manager)**

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (for zsh - default on macOS)
export PATH="$HOME/.cargo/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
uv --version
```

#### **Step 4: Install Network Automation Libraries**

```bash
# Core libraries
pip3 install nornir nornir-utils nornir-netmiko nornir-napalm

# Optional but recommended
pip3 install textfsm ntc-templates jinja2 pyyaml
```

---

### **For Windows Users (WSL)**

#### **Step 1: Update WSL and Install Python**

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 (recommended)
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Verify installation
python3.11 --version  # Should show 3.11.x
git --version
```

### **Step 2: Install uv (Modern Python Package Manager)**

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
uv --version
```

### **Step 3: Install Network Automation Libraries**

```bash
# Core libraries
pip3 install nornir nornir-utils nornir-netmiko nornir-napalm

# Optional but recommended
pip3 install textfsm ntc-templates jinja2 pyyaml
```

---

### **For Linux Users**

#### **Step 1: Update System and Install Python**

**For Debian/Ubuntu:**

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Verify installation
python3.11 --version  # Should show 3.11.x
git --version
```

**For RHEL/CentOS/Fedora:**

```bash
# Update system
sudo yum update -y  # RHEL/CentOS
# OR
sudo dnf update -y  # Fedora

# Install Python 3.11
sudo yum install python3.11 python3-pip git -y  # RHEL/CentOS
# OR
sudo dnf install python3.11 python3-pip git -y  # Fedora

# Verify installation
python3.11 --version
git --version
```

#### **Step 2: Install uv (Modern Python Package Manager)**

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
uv --version
```

#### **Step 3: Install Network Automation Libraries**

```bash
# Core libraries
pip3 install nornir nornir-utils nornir-netmiko nornir-napalm

# Optional but recommended
pip3 install textfsm ntc-templates jinja2 pyyaml
```

---

## **Installation**

### **Option 1: Install Your Enhanced NornFlow (Recommended)**

```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone your enhanced repository
git clone --recurse-submodules https://github.com/YOUR_USERNAME/n8n.git
cd n8n/nornflow-netops

# Install with uv
uv sync
uv pip install -e .

# Verify installation
nornflow --version  # Should show 0.4.0
```

### **Option 2: Install Official NornFlow from PyPI**

```bash
# Install from PyPI (official version only, no custom enhancements)
pip install nornflow

# Verify
nornflow --version
```

---

## **Project Initialization**

### **Create a New Project**

```bash
# Create project directory
mkdir ~/projects/my-network-automation
cd ~/projects/my-network-automation

# Initialize NornFlow project
nornflow init
```

**Generated structure:**
```
my-network-automation/
├── inventory/
│   ├── hosts.yaml
│   ├── groups.yaml
│   └── defaults.yaml
├── tasks/
├── workflows/
├── templates/
├── nornflow.yaml
└── .gitignore
```

### **Create Additional Directories**

```bash
# Create additional directories for organization
mkdir -p configs/backups
mkdir -p logs
mkdir -p documentation
mkdir -p tests
```

---

## **Inventory Configuration**

### **1. Configure Devices (hosts.yaml)**

```bash
nano inventory/hosts.yaml
```

```yaml
---
# Switches
switch-01:
  hostname: 192.168.1.10
  platform: ios
  groups:
    - switches
    - access
  data:
    site: datacenter-1
    role: access-switch

switch-02:
  hostname: 192.168.1.11
  platform: ios
  groups:
    - switches
    - access
  data:
    site: datacenter-1
    role: access-switch

# Routers
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

### **2. Configure Groups (groups.yaml)**

```bash
nano inventory/groups.yaml
```

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

access:
  data:
    priority: medium

edge:
  data:
    priority: high
```

### **3. Configure Defaults (defaults.yaml)**

```bash
nano inventory/defaults.yaml
```

```yaml
---
username: admin
password: ${NETWORK_PASSWORD}
platform: ios

connection_options:
  netmiko:
    extras:
      conn_timeout: 10
      auth_timeout: 10

data:
  domain: company.local
  ntp_servers:
    - 10.0.0.1
  dns_servers:
    - 8.8.8.8
```

### **4. Set Up Environment Variables**

```bash
# Create .env file
nano .env
```

```bash
# Network credentials
NETWORK_PASSWORD=YourPassword123
NETWORK_ENABLE_PASSWORD=YourEnablePassword

# Integration credentials
NETBOX_TOKEN=your-netbox-token
SERVICENOW_USER=your-snow-user
SERVICENOW_PASS=your-snow-pass
```

```bash
# Load environment variables
export $(cat .env | xargs)

# Or use direnv (recommended)
sudo apt install direnv
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
echo 'export $(cat .env | xargs)' > .envrc
direnv allow
```

---

## **Creating Workflows**

### **1. Simple Backup Workflow**

```bash
nano workflows/backup_devices.yaml
```

```yaml
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

### **2. Configuration Deployment Workflow**

```bash
nano workflows/deploy_config.yaml
```

```yaml
---
workflow:
  name: "Deploy Configuration"
  failure_strategy: "skip-failed"
  
  tasks:
    - name: backup_config
      task: backup_config
      args:
        backup_dir: "configs/backups/pre-deploy"
    
    - name: deploy_config
      task: deploy_config
      args:
        template_file: "templates/{{ host.platform }}/config.j2"
        backup_before: false
        validate_after: true
        rollback_on_error: true
      retry:
        max_attempts: 3
        delay: 5
```

---

## **Running Workflows**

### **Basic Commands**

```bash
# Show available devices
nornflow show --hosts

# Show available tasks
nornflow show --tasks

# Show available workflows
nornflow show --workflows

# Run a workflow
nornflow run workflows/backup_devices.yaml

# Run on specific hosts
nornflow run workflows/backup_devices.yaml --hosts switch-01,switch-02

# Run on a group
nornflow run workflows/backup_devices.yaml --groups switches

# Dry run (don't execute)
nornflow run workflows/backup_devices.yaml --dry-run

# Override variables
nornflow run workflows/backup_devices.yaml --set backup_dir=/tmp/backups
```

### **Check Exit Codes (v0.4.0)**

```bash
# Run and check exit code
nornflow run workflows/backup_devices.yaml
echo $?

# Exit codes:
# 0 = All hosts succeeded
# 1-100 = Percentage of failed hosts
# 101+ = Internal error
```

---

## **Using Custom Enhancements**

### **NetBox Integration**

```yaml
workflow:
  name: "NetBox Sync"
  vars:
    netbox_config:
      url: "https://netbox.company.com"
      token: "${NETBOX_TOKEN}"
  
  tasks:
    - name: netbox_get_device
      task: netbox_get_device
      args:
        device_name: "{{ host.name }}"
        netbox_config: "{{ netbox_config }}"
```

### **Git Integration**

```yaml
workflow:
  name: "Git Backup"
  vars:
    git_config:
      repo_path: "/opt/network-configs"
      author_name: "NornFlow"
      author_email: "nornflow@company.com"
  
  tasks:
    - name: git_commit_config
      task: git_commit_config
      args:
        config_content: "{{ backup_result.config }}"
        device_name: "{{ host.name }}"
        git_config: "{{ git_config }}"
```

---

## **Troubleshooting**

### **Common Issues (All Platforms)**

**1. Command not found: nornflow**
```bash
# Ensure PATH is set
export PATH="$HOME/.local/bin:$PATH"
# Or reinstall
pip install --user nornflow
```

**2. Connection timeout**
```bash
# Increase timeout in defaults.yaml
connection_options:
  netmiko:
    extras:
      conn_timeout: 30
```

**3. Authentication failed**
```bash
# Verify credentials in .env
# Check environment variables are loaded
echo $NETWORK_PASSWORD
```

**4. Module not found**
```bash
# Install missing dependencies
pip install nornir-netmiko nornir-napalm
```

---

### **macOS-Specific Issues**

**1. Python version conflicts**
```bash
# Use python3.11 explicitly
python3.11 -m pip install nornflow

# Or create alias
echo 'alias python=python3.11' >> ~/.zshrc
source ~/.zshrc
```

**2. SSL certificate errors**
```bash
# Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command

# Or use Homebrew Python
brew reinstall python@3.11
```

**3. Permission denied errors**
```bash
# Use --user flag
pip3 install --user nornflow

# Or fix permissions
sudo chown -R $(whoami) /usr/local/lib/python3.11
```

**4. Xcode Command Line Tools missing**
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

---

### **Windows/WSL-Specific Issues**

**1. WSL not installed**
```powershell
# In PowerShell (as Administrator)
wsl --install
# Restart computer
```

**2. Python not found in WSL**
```bash
# Update package lists
sudo apt update
# Install Python
sudo apt install python3.11 python3-pip
```

**3. Network connectivity issues**
```bash
# Check WSL networking
ping 8.8.8.8

# If fails, restart WSL networking
# In PowerShell (as Administrator):
wsl --shutdown
# Then restart WSL
```

**4. File permission issues**
```bash
# WSL files should be in WSL filesystem, not Windows
# Move project to WSL home
mv /mnt/c/projects/my-project ~/projects/
```

---

### **Linux-Specific Issues**

**1. Python 3.11 not available**
```bash
# Add deadsnakes PPA (Ubuntu/Debian)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv

# Or compile from source
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
tar -xf Python-3.11.0.tgz
cd Python-3.11.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

**2. Permission denied for pip**
```bash
# Use --user flag
pip3 install --user nornflow

# Or use virtual environment (recommended)
python3.11 -m venv venv
source venv/bin/activate
pip install nornflow
```

**3. Missing development headers**
```bash
# Debian/Ubuntu
sudo apt install python3.11-dev build-essential

# RHEL/CentOS
sudo yum install python3-devel gcc
```

**4. SELinux blocking connections**
```bash
# Check SELinux status
getenforce

# Temporarily disable (for testing)
sudo setenforce 0

# Or configure SELinux policies
sudo setsebool -P httpd_can_network_connect 1
```

---

## **Next Steps**

1. ✅ Install NornFlow
2. ✅ Create project
3. ✅ Configure inventory
4. ✅ Create workflows
5. ✅ Run your first automation
6. 🚀 Explore integrations (NetBox, Git, ServiceNow)
7. 🚀 Set up scheduling
8. 🚀 Deploy monitoring dashboard

---

**For the N8N Stack Generator, see:** `N8N_NETWORK_STACK_GENERATOR.md`

