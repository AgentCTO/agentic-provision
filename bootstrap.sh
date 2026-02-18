#!/bin/bash
#
# agentic-provision bootstrap script
# One command to get an AI agent ready to provision your Mac
#
# Usage: curl -fsSL https://raw.githubusercontent.com/AgentCTO/agentic-provision/main/bootstrap.sh | bash
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() { echo -e "${BLUE}▶${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}        🤖 Agentic Provision                ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}   AI-assisted Mac development setup        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# ------------------------------------------------------------------------------
# Preflight checks
# ------------------------------------------------------------------------------

# macOS only
if [[ "$(uname)" != "Darwin" ]]; then
    print_error "This script is designed for macOS only."
    exit 1
fi

print_success "Running on macOS $(sw_vers -productVersion)"

# ------------------------------------------------------------------------------
# Xcode Command Line Tools
# ------------------------------------------------------------------------------

if ! xcode-select -p &>/dev/null; then
    print_step "Installing Xcode Command Line Tools..."
    print_warning "A dialog will appear. Click 'Install' and wait for completion."
    xcode-select --install

    # Wait for installation
    echo ""
    read -p "Press Enter once the installation completes..."

    if ! xcode-select -p &>/dev/null; then
        print_error "Xcode Command Line Tools installation failed."
        exit 1
    fi
fi
print_success "Xcode Command Line Tools installed"

# ------------------------------------------------------------------------------
# Homebrew
# ------------------------------------------------------------------------------

if ! command -v brew &>/dev/null; then
    print_step "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add brew to PATH for this session (Apple Silicon vs Intel)
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f "/usr/local/bin/brew" ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
fi
print_success "Homebrew installed ($(brew --version | head -1))"

# ------------------------------------------------------------------------------
# Claude Code
# ------------------------------------------------------------------------------

if ! command -v claude &>/dev/null; then
    print_step "Installing Claude Code..."
    brew install --cask claude-code
fi
print_success "Claude Code installed ($(claude --version 2>/dev/null | head -1))"

# ------------------------------------------------------------------------------
# Python (via Homebrew for consistency)
# ------------------------------------------------------------------------------

if ! brew list python@3.11 &>/dev/null; then
    print_step "Installing Python 3.11..."
    brew install python@3.11
fi
print_success "Python 3.11 installed"

# Get the Homebrew Python path
PYTHON_PATH="$(brew --prefix python@3.11)/bin/python3.11"

# ------------------------------------------------------------------------------
# Python Environment
# ------------------------------------------------------------------------------

print_step "Setting up Python environment..."

# Create a virtual environment for the provisioner
PROVISION_DIR="${HOME}/.agentic-provision"
VENV_DIR="${PROVISION_DIR}/venv"

if [[ ! -d "$VENV_DIR" ]]; then
    mkdir -p "$PROVISION_DIR"
    "$PYTHON_PATH" -m venv "$VENV_DIR"
fi

# Activate and install dependencies
source "${VENV_DIR}/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet anthropic pyyaml

print_success "Python environment configured"

# ------------------------------------------------------------------------------
# Anthropic API Key
# ------------------------------------------------------------------------------

SHELL_RC="${HOME}/.zshrc"
[[ -f "${HOME}/.bashrc" ]] && [[ ! -f "${HOME}/.zshrc" ]] && SHELL_RC="${HOME}/.bashrc"

if [[ -n "$ANTHROPIC_API_KEY" ]]; then
    print_success "ANTHROPIC_API_KEY is set"
elif grep -q "ANTHROPIC_API_KEY" "$SHELL_RC" 2>/dev/null; then
    print_success "ANTHROPIC_API_KEY found in $SHELL_RC"
else
    print_warning "ANTHROPIC_API_KEY is not set"
    echo ""
    echo "  Get your key at: https://console.anthropic.com/settings/keys"
    echo ""
    read -p "  Enter your Anthropic API key (or press Enter to skip): " api_key
    if [[ -n "$api_key" ]]; then
        echo "" >> "$SHELL_RC"
        echo "# Anthropic API Key" >> "$SHELL_RC"
        echo "export ANTHROPIC_API_KEY='$api_key'" >> "$SHELL_RC"
        export ANTHROPIC_API_KEY="$api_key"
        print_success "API key saved to $SHELL_RC"
    else
        print_warning "Skipped — set it later: export ANTHROPIC_API_KEY='sk-ant-...'"
    fi
fi

# ------------------------------------------------------------------------------
# Create directory structure
# ------------------------------------------------------------------------------

print_step "Creating directory structure..."

KNOWLEDGE_DIR="${PROVISION_DIR}/knowledge"
TASKS_DIR="${PROVISION_DIR}/tasks"
SESSIONS_DIR="${PROVISION_DIR}/sessions"
LOGS_DIR="${PROVISION_DIR}/logs"

# Create all required directories
mkdir -p "$KNOWLEDGE_DIR"
mkdir -p "${TASKS_DIR}/core"
mkdir -p "${TASKS_DIR}/profiles"
mkdir -p "${TASKS_DIR}/custom"
mkdir -p "${SESSIONS_DIR}/active"
mkdir -p "${SESSIONS_DIR}/completed"
mkdir -p "${SESSIONS_DIR}/failed"
mkdir -p "$LOGS_DIR"

print_success "Directory structure created"

# ------------------------------------------------------------------------------
# Download knowledge base and task manifests
# ------------------------------------------------------------------------------

print_step "Downloading knowledge base..."

# If running from curl|bash, download knowledge files
# If running locally, copy from repo
REPO_URL="https://raw.githubusercontent.com/AgentCTO/agentic-provision/main"

LIB_DIR="${PROVISION_DIR}/lib"
mkdir -p "$LIB_DIR"

if [[ -f "./knowledge/system-prompt.md" ]]; then
    # Running from local repo
    cp -r ./knowledge/* "$KNOWLEDGE_DIR/"

    # Copy task manifests
    if [[ -d "./tasks" ]]; then
        cp -r ./tasks/* "$TASKS_DIR/"
    fi

    # Copy lib modules
    if [[ -d "./lib" ]]; then
        cp -r ./lib/* "$LIB_DIR/"
    fi
else
    # Running from curl|bash - download files

    # Knowledge files
    KNOWLEDGE_FILES=(
        "system-prompt.md"
        "macos-best-practices.md"
        "common-pitfalls.md"
        "session-schema.md"
        "task-manifest-schema.md"
        "provisioning-approaches.md"
        "tools-reference.md"
        "brewfile-templates.md"
        "macos-defaults-reference.md"
        "github-repositories.md"
    )

    for file in "${KNOWLEDGE_FILES[@]}"; do
        curl -fsSL "${REPO_URL}/knowledge/${file}" -o "${KNOWLEDGE_DIR}/${file}" 2>/dev/null || true
    done

    # Core task manifests
    CORE_TASKS=(
        "package-managers.yaml"
        "version-managers.yaml"
        "editors.yaml"
        "databases.yaml"
        "containers.yaml"
        "shells.yaml"
        "git-setup.yaml"
        "cli-tools.yaml"
    )

    for file in "${CORE_TASKS[@]}"; do
        curl -fsSL "${REPO_URL}/tasks/core/${file}" -o "${TASKS_DIR}/core/${file}" 2>/dev/null || true
    done

    # Profile manifests
    PROFILES=(
        "fullstack-web.yaml"
        "data-science.yaml"
        "mobile-dev.yaml"
        "devops.yaml"
    )

    for file in "${PROFILES[@]}"; do
        curl -fsSL "${REPO_URL}/tasks/profiles/${file}" -o "${TASKS_DIR}/profiles/${file}" 2>/dev/null || true
    done

    # Download lib modules
    curl -fsSL "${REPO_URL}/lib/state_manager.py" -o "${LIB_DIR}/state_manager.py" 2>/dev/null || true
    curl -fsSL "${REPO_URL}/lib/provision.py" -o "${LIB_DIR}/provision.py" 2>/dev/null || true
fi

print_success "Knowledge base and task manifests ready"

# ------------------------------------------------------------------------------
# Create launcher script
# ------------------------------------------------------------------------------

LAUNCHER="${PROVISION_DIR}/provision"

cat > "$LAUNCHER" << 'LAUNCHER_SCRIPT'
#!/bin/bash
#
# Agentic Provision launcher
#
# Usage:
#   provision                    # Default: confirm each command
#   provision --auto-approve     # Skip command confirmations
#   provision -y                 # Same as --auto-approve
#
# Requires: Claude Code CLI (brew install --cask claude-code)
#

PROVISION_DIR="${HOME}/.agentic-provision"
VENV_DIR="${PROVISION_DIR}/venv"
LIB_DIR="${PROVISION_DIR}/lib"

# Check for Claude Code CLI
if ! command -v claude &>/dev/null; then
    echo "Error: Claude Code CLI not found."
    echo ""
    echo "Install it with:"
    echo "  brew install --cask claude-code"
    echo ""
    echo "Or visit: https://claude.ai/download"
    exit 1
fi

# Activate virtual environment
source "${VENV_DIR}/bin/activate"

# Set environment variables
export AGENTIC_PROVISION_DIR="${PROVISION_DIR}"
export PYTHONPATH="${LIB_DIR}:${PYTHONPATH}"

# Run the provisioner
python "${LIB_DIR}/provision.py" "$@"
LAUNCHER_SCRIPT

chmod +x "$LAUNCHER"

# Add to PATH if not already there
if ! grep -q "agentic-provision" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# Agentic Provision" >> "$SHELL_RC"
    echo 'export PATH="${HOME}/.agentic-provision:${PATH}"' >> "$SHELL_RC"
fi

print_success "Launcher script created"

# ------------------------------------------------------------------------------
# Done
# ------------------------------------------------------------------------------

echo ""
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Installation complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════${NC}"
echo ""
echo "  Run later:  ${BLUE}provision${NC}"
echo "  Options:    provision -y   (skip confirmations)"
echo ""

# Authenticate Claude Code if needed
if ! claude auth status &>/dev/null 2>&1; then
    print_warning "Claude Code needs authentication. Run 'claude' once to sign in."
    echo ""
fi

read -p "Start the provisioner now? [Y/n] " launch_now
echo ""
if [[ "$launch_now" =~ ^[Nn] ]]; then
    echo "  When ready, open a new terminal and run: ${BLUE}provision${NC}"
    echo ""
else
    # Reload shell config so PATH includes the launcher
    export PATH="${HOME}/.agentic-provision:${PATH}"
    exec "$LAUNCHER"
fi
