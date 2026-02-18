#!/bin/bash
#
# agentic-provision bootstrap script
# One command to get an AI agent ready to provision your Mac
#
# Usage: curl -fsSL https://raw.githubusercontent.com/AgentCTO/agentic-provision/refs/heads/main/bootstrap.sh | bash
#

set -e

# Colors for output
RED=$(printf '\033[0;31m')
GREEN=$(printf '\033[0;32m')
YELLOW=$(printf '\033[0;33m')
BLUE=$(printf '\033[0;34m')
NC=$(printf '\033[0m')

print_step() { echo "${BLUE}▶${NC} $1"; }
print_success() { echo "${GREEN}✓${NC} $1"; }
print_warning() { echo "${YELLOW}⚠${NC} $1"; }
print_error() { echo "${RED}✗${NC} $1"; }

echo ""
echo "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo "${BLUE}║${NC}        🤖 Agentic Provision                ${BLUE}║${NC}"
echo "${BLUE}║${NC}   AI-assisted Mac development setup        ${BLUE}║${NC}"
echo "${BLUE}╚════════════════════════════════════════════╝${NC}"
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

# Verify and cache administrator credentials upfront
print_step "Verifying administrator access..."
if ! sudo -v </dev/tty; then
    print_error "Administrator privileges are required."
    print_error "Check System Settings > Users & Groups and ensure your account type is Administrator."
    exit 1
fi
print_success "Administrator access confirmed"

# ------------------------------------------------------------------------------
# Xcode Command Line Tools
# ------------------------------------------------------------------------------

if ! xcode-select -p &>/dev/null; then
    print_step "Installing Xcode Command Line Tools..."
    print_warning "A dialog will appear — click 'Install' to continue."
    xcode-select --install 2>/dev/null || true

    print_step "Waiting for installation to complete (this may take several minutes)..."
    ATTEMPTS=0
    until xcode-select -p &>/dev/null; do
        sleep 5
        ATTEMPTS=$((ATTEMPTS + 1))
        if [[ $ATTEMPTS -ge 360 ]]; then
            print_error "Timed out waiting for Xcode Command Line Tools (30 min). Re-run the script to retry."
            exit 1
        fi
    done
fi
print_success "Xcode Command Line Tools installed"

# ------------------------------------------------------------------------------
# Homebrew
# ------------------------------------------------------------------------------

if ! command -v brew &>/dev/null; then
    print_step "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Add Homebrew to PATH for this session and persist to shell profile
if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
    BREW_SHELLENV='eval "$(/opt/homebrew/bin/brew shellenv)"'
elif [[ -f "/usr/local/bin/brew" ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
    BREW_SHELLENV='eval "$(/usr/local/bin/brew shellenv)"'
fi

if [[ -n "$BREW_SHELLENV" ]] && ! grep -qF "brew shellenv" "${HOME}/.zprofile" 2>/dev/null; then
    echo "" >> "${HOME}/.zprofile"
    echo "# Homebrew" >> "${HOME}/.zprofile"
    echo "$BREW_SHELLENV" >> "${HOME}/.zprofile"
    print_success "Homebrew added to PATH in ~/.zprofile"
fi

print_success "Homebrew installed ($(brew --version | head -1))"

# ------------------------------------------------------------------------------
# Claude Code
# ------------------------------------------------------------------------------

if ! command -v claude &>/dev/null; then
    print_step "Installing Claude Code..."
    brew install --cask claude-code
fi
print_success "Claude Code installed"

PROVISION_DIR="${HOME}/.agentic-provision"

SHELL_RC="${HOME}/.zshrc"
[[ -f "${HOME}/.bashrc" ]] && [[ ! -f "${HOME}/.zshrc" ]] && SHELL_RC="${HOME}/.bashrc"

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

# Copy system prompt as CLAUDE.md so Claude Code loads it automatically
# --system-prompt flag only works in print mode; CLAUDE.md is loaded in interactive mode
cp "${KNOWLEDGE_DIR}/system-prompt.md" "${PROVISION_DIR}/CLAUDE.md"
print_success "System prompt configured"

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
#   provision        # Start or resume a provisioning session
#

PROVISION_DIR="${HOME}/.agentic-provision"

if ! command -v claude &>/dev/null; then
    echo "Error: Claude Code not found."
    echo "Install: brew install --cask claude-code"
    exit 1
fi

# cd into provision dir so Claude loads CLAUDE.md as context automatically
# (--system-prompt flag is print-mode only and doesn't work in interactive mode)
cd "${PROVISION_DIR}"

echo ""
echo "Starting Agentic Provision..."
echo "Type 'begin' and press Enter to start."
echo ""

exec claude
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
echo "${GREEN}════════════════════════════════════════════${NC}"
echo "${GREEN}  Bootstrap complete!${NC}"
echo "${GREEN}════════════════════════════════════════════${NC}"
echo ""
echo "  Next steps:"
echo ""
echo "  1. Open a new terminal"
echo ""
echo "  2. Authenticate Claude Code:"
echo "     ${BLUE}claude${NC}"
echo ""
echo "  3. Start the provisioner:"
echo "     ${BLUE}provision${NC}"
echo ""
