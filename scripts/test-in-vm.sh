#!/bin/bash
# Run full end-to-end tests in a Tart macOS VM
# Requires: brew install cirruslabs/cli/tart
# Usage: ./test-in-vm.sh [--keep]

set -e

VM_NAME="provision-test"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_PATH="$(dirname "$SCRIPT_DIR")"
KEEP_VM=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep)
            KEEP_VM=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check for Tart
if ! command -v tart &>/dev/null; then
    echo "Tart not found. Install with: brew install cirruslabs/cli/tart"
    exit 1
fi

# Cleanup function
cleanup() {
    if [ "$KEEP_VM" = false ]; then
        echo "Cleaning up VM..."
        tart stop "$VM_NAME" 2>/dev/null || true
        tart delete "$VM_NAME" 2>/dev/null || true
    else
        echo "Keeping VM '$VM_NAME' (use 'tart delete $VM_NAME' to remove)"
    fi
}

trap cleanup EXIT

echo "=== Agentic Provision VM Test ==="
echo ""

# Check if base image exists
if ! tart list | grep -q "macos-sequoia-base"; then
    echo "Pulling macOS base image (this may take a while)..."
    tart clone ghcr.io/cirruslabs/macos-sequoia-base:latest macos-sequoia-base
fi

# Create fresh VM
echo "Creating fresh VM from base image..."
tart delete "$VM_NAME" 2>/dev/null || true
tart clone macos-sequoia-base "$VM_NAME"

# Start VM in background
echo "Starting VM (this takes ~60 seconds)..."
tart run "$VM_NAME" --no-graphics &
VM_PID=$!

# Wait for VM to boot
echo "Waiting for VM to boot..."
sleep 60

# Get VM IP
VM_IP=$(tart ip "$VM_NAME" 2>/dev/null)
if [ -z "$VM_IP" ]; then
    echo "Failed to get VM IP. VM may not have booted correctly."
    exit 1
fi
echo "VM IP: $VM_IP"

# Wait for SSH to be available
echo "Waiting for SSH..."
for i in {1..30}; do
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "admin@$VM_IP" "echo ready" &>/dev/null; then
        break
    fi
    sleep 2
done

# Copy project to VM
echo "Copying project to VM..."
scp -r -o StrictHostKeyChecking=no "$REPO_PATH" "admin@$VM_IP:~/agentic-provision"

# Run tests in VM
echo ""
echo "=== Running Tests in VM ==="
ssh -o StrictHostKeyChecking=no "admin@$VM_IP" << 'REMOTE_SCRIPT'
set -e
cd ~/agentic-provision

echo ""
echo "=== Step 1: Install Homebrew ==="
if ! command -v brew &>/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
fi
echo "Homebrew: $(brew --version | head -1)"

echo ""
echo "=== Step 2: Install Python (for test scripts) ==="
brew install python@3.11 pyyaml 2>/dev/null || true
pip3 install pyyaml 2>/dev/null || true

echo ""
echo "=== Step 3: Validate Manifests ==="
python3 scripts/validate-manifests.py

echo ""
echo "=== Step 4: Validate Profile References ==="
python3 scripts/validate-profile-refs.py

echo ""
echo "=== Step 5: Detection Tests (Pre-Install) ==="
python3 scripts/test-detection.py --category cli-tools

echo ""
echo "=== Step 6: Install Sample CLI Tools ==="
brew install jq ripgrep fzf fd bat eza

echo ""
echo "=== Step 7: Detection Tests (Post-Install) ==="
python3 scripts/test-detection.py --category cli-tools --verbose

echo ""
echo "=== Step 8: Install Sample Cask (VS Code) ==="
brew install --cask visual-studio-code

echo ""
echo "=== Step 9: Test Editor Detection ==="
python3 scripts/test-detection.py --category editors --verbose

echo ""
echo "=== All VM Tests Complete ==="
REMOTE_SCRIPT

echo ""
echo "=== VM Test Suite Finished ==="

# Stop VM
kill $VM_PID 2>/dev/null || true
tart stop "$VM_NAME" 2>/dev/null || true

if [ "$KEEP_VM" = true ]; then
    echo ""
    echo "VM kept. To access: tart run $VM_NAME"
    echo "To delete: tart delete $VM_NAME"
fi
