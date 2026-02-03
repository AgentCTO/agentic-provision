#!/bin/bash
# Run provisioning tests as the isolated test user
# Usage: sudo ./test-as-user.sh

set -e

TEST_USER="provisiontest"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_PATH="$(dirname "$SCRIPT_DIR")"

if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo: sudo $0"
    exit 1
fi

# Check if test user exists
if ! dscl . -read /Users/$TEST_USER &>/dev/null; then
    echo "Test user does not exist. Run setup-test-user.sh first."
    exit 1
fi

echo "Running tests as $TEST_USER..."
echo "Repository: $REPO_PATH"
echo ""

# Run tests as test user
sudo -u $TEST_USER -i << EOF
cd "$REPO_PATH"

echo "=== Environment Check ==="
echo "User: \$(whoami)"
echo "Home: \$HOME"
echo "Shell: \$SHELL"

# Ensure Homebrew is available
if [ -d /opt/homebrew ]; then
    eval "\$(/opt/homebrew/bin/brew shellenv)"
elif [ -d /usr/local/Homebrew ]; then
    eval "\$(/usr/local/bin/brew shellenv)"
fi

if command -v brew &>/dev/null; then
    echo "Homebrew: \$(brew --version | head -1)"
else
    echo "Homebrew: NOT FOUND"
    echo "Install Homebrew first"
    exit 1
fi

echo ""
echo "=== Testing Detection Commands ==="
python3 scripts/test-detection.py --verbose

echo ""
echo "=== Testing Manifest Validation ==="
python3 scripts/validate-manifests.py

echo ""
echo "=== Testing Profile References ==="
python3 scripts/validate-profile-refs.py

echo ""
echo "=== Sample CLI Installation Test ==="
echo "Installing: jq, bat (safe CLI tools)"

if ! command -v jq &>/dev/null; then
    brew install jq
    echo "✓ jq installed"
else
    echo "○ jq already installed"
fi

if ! command -v bat &>/dev/null; then
    brew install bat
    echo "✓ bat installed"
else
    echo "○ bat already installed"
fi

echo ""
echo "=== Re-testing Detection (Post-Install) ==="
python3 scripts/test-detection.py --category cli-tools --verbose

echo ""
echo "=== Tests Complete ==="
EOF

echo ""
echo "Test run finished."
