#!/bin/bash

# NornFlow NetOps Fork Setup Script
# This script helps you set up the nornflow-netops repository for development

set -e  # Exit on any error

echo "🚀 NornFlow NetOps Setup Script"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Set the repository details
GITHUB_USERNAME="chasewoodard93"
REPO_NAME="nornflow-netops"

print_step "Setting up NornFlow NetOps repository"
print_step "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Check if we're already in the repository directory
if [ -d ".git" ] && [ "$(basename $(pwd))" = "$REPO_NAME" ]; then
    print_status "Already in the repository directory"
else
    # Step 1: Clone the forked repository
    print_step "1. Cloning the repository..."
    if [ -d "$REPO_NAME" ]; then
        print_warning "Directory $REPO_NAME already exists. Entering directory."
        cd "$REPO_NAME"
    else
        git clone "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        cd "$REPO_NAME"
        print_status "Repository cloned successfully"
    fi
fi

# Step 2: Add upstream remote
print_step "2. Adding upstream remote..."
if git remote get-url upstream >/dev/null 2>&1; then
    print_warning "Upstream remote already exists"
else
    git remote add upstream https://github.com/theandrelima/nornflow.git
    print_status "Upstream remote added"
fi

# Step 3: Check if uv is installed
print_step "3. Checking for uv package manager..."
if ! command -v uv &> /dev/null; then
    print_warning "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    print_status "uv installed successfully"
else
    print_status "uv is already installed"
fi

# Step 4: Create virtual environment
print_step "4. Setting up virtual environment..."
if [ -d ".venv" ]; then
    print_warning "Virtual environment already exists"
else
    uv venv
    print_status "Virtual environment created"
fi

# Step 5: Install dependencies
print_step "5. Installing dependencies..."
source .venv/bin/activate || source .venv/Scripts/activate  # Windows compatibility
uv pip install -e ".[dev,manual-tests]"
print_status "Dependencies installed successfully"

# Step 6: Verify installation
print_step "6. Verifying installation..."
if .venv/bin/nornflow --help >/dev/null 2>&1 || .venv/Scripts/nornflow --help >/dev/null 2>&1; then
    print_status "NornFlow installation verified successfully"
else
    print_error "NornFlow installation verification failed"
    exit 1
fi

# Step 7: Create development branch
print_step "7. Creating development branch..."
git checkout -b development 2>/dev/null || git checkout development
print_status "Development branch ready"

# Step 8: Create enhancement planning directory
print_step "8. Setting up enhancement planning..."
mkdir -p docs/enhancements
mkdir -p enhancements/network-tasks
mkdir -p enhancements/workflow-control
mkdir -p enhancements/integrations
mkdir -p enhancements/testing
mkdir -p enhancements/user-experience

print_status "Enhancement directories created"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "Your NornFlow fork is ready for development!"
echo ""
echo "Next steps:"
echo "1. cd $REPO_NAME"
echo "2. source .venv/bin/activate  # (or .venv/Scripts/activate on Windows)"
echo "3. nornflow --help  # Verify everything works"
echo ""
echo "Repository structure:"
echo "- Original remote: upstream -> https://github.com/theandrelima/nornflow.git"
echo "- Your fork: origin -> https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "- Current branch: development"
echo ""
echo "Enhancement directories created in ./enhancements/"
echo ""
print_status "Happy coding! 🚀"
