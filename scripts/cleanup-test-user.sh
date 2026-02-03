#!/bin/bash
# Remove the test user created by setup-test-user.sh
# Usage: sudo ./cleanup-test-user.sh

set -e

TEST_USER="provisiontest"

if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo: sudo $0"
    exit 1
fi

echo "Removing test user: $TEST_USER"

# Check if user exists
if ! dscl . -read /Users/$TEST_USER &>/dev/null; then
    echo "User $TEST_USER does not exist."
    exit 0
fi

# Kill any processes owned by user
pkill -u $TEST_USER 2>/dev/null || true

# Remove from admin group
dscl . -delete /Groups/admin GroupMembership $TEST_USER 2>/dev/null || true

# Delete user
dscl . -delete /Users/$TEST_USER

# Remove home directory
rm -rf /Users/$TEST_USER

echo "Test user '$TEST_USER' removed."
