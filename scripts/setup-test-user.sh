#!/bin/bash
# Create an isolated test user for provisioning tests
# Usage: sudo ./setup-test-user.sh

set -e

TEST_USER="provisiontest"
TEST_UID=550

if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo: sudo $0"
    exit 1
fi

echo "Creating test user: $TEST_USER"

# Check if user exists
if dscl . -read /Users/$TEST_USER &>/dev/null; then
    echo "User $TEST_USER already exists. Delete first with cleanup-test-user.sh"
    exit 1
fi

# Create user
dscl . -create /Users/$TEST_USER
dscl . -create /Users/$TEST_USER UserShell /bin/zsh
dscl . -create /Users/$TEST_USER NFSHomeDirectory /Users/$TEST_USER
dscl . -create /Users/$TEST_USER UniqueID $TEST_UID
dscl . -create /Users/$TEST_USER PrimaryGroupID 20
dscl . -create /Users/$TEST_USER RealName "Provision Test"

# Set empty password for automation
dscl . -passwd /Users/$TEST_USER ""

# Create home directory
createhomedir -c -u $TEST_USER

# Add to admin group for brew access
dscl . -append /Groups/admin GroupMembership $TEST_USER

echo ""
echo "Test user '$TEST_USER' created successfully."
echo ""
echo "Usage:"
echo "  Switch to test user:  su - $TEST_USER"
echo "  Run test as user:     sudo -u $TEST_USER -i 'command'"
echo "  Delete test user:     sudo scripts/cleanup-test-user.sh"
echo ""
echo "Note: Homebrew (/opt/homebrew) is shared across users."
echo "      GUI apps in /Applications are also shared."
