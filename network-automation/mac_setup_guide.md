# NornFlow NetOps - Mac Setup Guide

## Prerequisites

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Git (if not already installed)
```bash
brew install git
```

## Quick Setup

### Option 1: Manual Setup (Recommended)

```bash
# 1. Create development directory
mkdir -p ~/Development/NetworkAutomation
cd ~/Development/NetworkAutomation

# 2. Clone your fork
git clone https://github.com/chasewoodard93/nornflow-netops.git
cd nornflow-netops

# 3. Add upstream remote
git remote add upstream https://github.com/theandrelima/nornflow.git

# 4. Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Add to PATH (add this to your ~/.zshrc or ~/.bash_profile)
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.zshrc  # or source ~/.bash_profile

# 5. Create virtual environment
uv venv

# 6. Activate virtual environment
source .venv/bin/activate

# 7. Install dependencies
uv pip install -e ".[dev,manual-tests]"

# 8. Verify installation
nornflow --help

# 9. Create development branch
git checkout -b development
```

### Option 2: Using the Setup Script

```bash
# Make the script executable and run it
chmod +x setup_nornflow_fork.sh
./setup_nornflow_fork.sh
```

## Development Workflow

### Daily Development
```bash
# Navigate to project
cd ~/Development/NetworkAutomation/nornflow-netops

# Activate virtual environment
source .venv/bin/activate

# Start coding!
```

### Keeping Your Fork Updated
```bash
# Fetch latest changes from upstream
git fetch upstream

# Merge upstream changes into your main branch
git checkout main
git merge upstream/main

# Push updates to your fork
git push origin main
```

### Working with Branches
```bash
# Create feature branch
git checkout -b feature/network-tasks

# Work on your changes...

# Commit and push
git add .
git commit -m "Add network automation tasks"
git push origin feature/network-tasks
```

## Project Structure

After setup, your project will have this structure:

```
nornflow-netops/
├── nornflow/                 # Core NornFlow code
├── tests/                    # Test files
├── docs/                     # Documentation
├── enhancements/             # Our enhancement work
│   ├── network-tasks/        # Network automation tasks
│   ├── workflow-control/     # Advanced workflow features
│   ├── integrations/         # External system integrations
│   ├── testing/              # Testing framework
│   └── user-experience/      # UX improvements
├── .venv/                    # Virtual environment
├── pyproject.toml           # Project configuration
└── README.md                # Project documentation
```

## Useful Commands

```bash
# Run tests
pytest

# Format code
black .
ruff check .

# Install new dependencies
uv pip install package-name

# Run NornFlow commands
nornflow --help
nornflow init
nornflow show --catalog
```

## IDE Setup

### VS Code (Recommended)
1. Install Python extension
2. Select interpreter: `Cmd+Shift+P` → "Python: Select Interpreter" → Choose `.venv/bin/python`
3. Install recommended extensions:
   - Python
   - Pylance
   - Black Formatter
   - Ruff

### PyCharm
1. Open project directory
2. Configure interpreter: Settings → Project → Python Interpreter → Add → Existing Environment → `.venv/bin/python`

## Troubleshooting

### Common Issues

**uv not found after installation:**
```bash
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.zshrc
```

**Permission denied on script:**
```bash
chmod +x setup_nornflow_fork.sh
```

**Virtual environment activation fails:**
```bash
# Try absolute path
source ~/Development/NetworkAutomation/nornflow-netops/.venv/bin/activate
```

**Dependencies installation fails:**
```bash
# Update uv first
uv self update
# Then try again
uv pip install -e ".[dev,manual-tests]"
```

## Next Steps

Once setup is complete, you're ready to start enhancing NornFlow! The enhancement tasks are organized in the `enhancements/` directory, and we'll work through them systematically.
