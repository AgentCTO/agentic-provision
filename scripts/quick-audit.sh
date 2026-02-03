#!/bin/bash
# Quick system audit without Python dependency
# Useful for bootstrap phase before Python/PyYAML are installed

set -e

echo "========================================================================"
echo "AGENTIC PROVISION - QUICK SYSTEM AUDIT"
echo "========================================================================"
echo "Timestamp: $(date -Iseconds)"
echo ""

# System info
echo "SYSTEM INFORMATION"
echo "----------------------------------------"
echo "  Hostname:        $(hostname -s)"
echo "  macOS:           $(sw_vers -productVersion)"
echo "  Architecture:    $(uname -m)"
echo "  Shell:           $SHELL"

# Xcode CLI
if xcode-select -p &>/dev/null; then
    echo "  Xcode CLI:       ✓ Installed"
else
    echo "  Xcode CLI:       ✗ Not installed"
fi

# Homebrew
if command -v brew &>/dev/null; then
    echo "  Homebrew:        ✓ $(brew --prefix)"
    BREW_INSTALLED=true
else
    echo "  Homebrew:        ✗ Not installed"
    BREW_INSTALLED=false
fi

echo ""

# Quick checks for common tools
echo "COMMON DEVELOPMENT TOOLS"
echo "----------------------------------------"

check_command() {
    local name="$1"
    local cmd="$2"
    local version_cmd="$3"

    if eval "$cmd" &>/dev/null; then
        if [ -n "$version_cmd" ]; then
            local ver=$(eval "$version_cmd" 2>/dev/null | head -1)
            printf "  ✓ %-20s %s\n" "$name" "$ver"
        else
            printf "  ✓ %-20s installed\n" "$name"
        fi
    else
        printf "  ○ %-20s not installed\n" "$name"
    fi
}

check_app() {
    local name="$1"
    local path="$2"

    if [ -d "$path" ]; then
        printf "  ✓ %-20s installed\n" "$name"
    else
        printf "  ○ %-20s not installed\n" "$name"
    fi
}

echo ""
echo "  [Version Managers]"
check_command "nvm" '[ -s "$HOME/.nvm/nvm.sh" ]' ""
check_command "fnm" "command -v fnm" "fnm --version"
check_command "pyenv" "command -v pyenv" "pyenv --version"
check_command "rbenv" "command -v rbenv" "rbenv --version"
check_command "mise" "command -v mise" "mise --version"

echo ""
echo "  [Languages & Runtimes]"
check_command "Node.js" "command -v node" "node --version"
check_command "Python 3" "command -v python3" "python3 --version"
check_command "Ruby" "command -v ruby" "ruby --version"
check_command "Go" "command -v go" "go version"
check_command "Rust" "command -v rustc" "rustc --version"
check_command "Java" "command -v java" "java --version 2>&1 | head -1"

echo ""
echo "  [Editors]"
check_app "VS Code" "/Applications/Visual Studio Code.app"
check_app "Cursor" "/Applications/Cursor.app"
check_command "Neovim" "command -v nvim" "nvim --version | head -1"
check_command "Vim" "command -v vim" "vim --version | head -1"
check_app "Sublime Text" "/Applications/Sublime Text.app"
check_app "WebStorm" "/Applications/WebStorm.app"
check_app "PyCharm" "/Applications/PyCharm.app"

echo ""
echo "  [Containers]"
check_app "Docker Desktop" "/Applications/Docker.app"
check_command "docker" "command -v docker" "docker --version"
check_command "colima" "command -v colima" "colima version"
check_command "podman" "command -v podman" "podman --version"
check_command "kubectl" "command -v kubectl" "kubectl version --client -o yaml 2>/dev/null | grep gitVersion | cut -d: -f2"

echo ""
echo "  [Databases]"
check_command "PostgreSQL" "command -v psql" "psql --version"
check_command "MySQL" "command -v mysql" "mysql --version"
check_command "MongoDB" "command -v mongod" "mongod --version | head -1"
check_command "Redis" "command -v redis-server" "redis-server --version"
check_command "SQLite" "command -v sqlite3" "sqlite3 --version"

echo ""
echo "  [CLI Tools]"
check_command "git" "command -v git" "git --version"
check_command "gh (GitHub)" "command -v gh" "gh --version | head -1"
check_command "jq" "command -v jq" "jq --version"
check_command "ripgrep" "command -v rg" "rg --version | head -1"
check_command "fzf" "command -v fzf" "fzf --version"
check_command "fd" "command -v fd" "fd --version"
check_command "bat" "command -v bat" "bat --version | head -1"
check_command "eza" "command -v eza" "eza --version | head -1"
check_command "htop" "command -v htop" "htop --version | head -1"
check_command "tmux" "command -v tmux" "tmux -V"

echo ""
echo "  [AI Tools]"
check_command "Claude Code" "command -v claude" "claude --version 2>/dev/null || echo 'installed'"
check_command "Ollama" "command -v ollama" "ollama --version"
check_app "LM Studio" "/Applications/LM Studio.app"
check_app "ChatGPT" "/Applications/ChatGPT.app"

echo ""
echo "  [Shells & Prompts]"
check_command "Starship" "command -v starship" "starship --version"
check_command "Oh My Zsh" '[ -d "$HOME/.oh-my-zsh" ]' ""
check_command "Powerlevel10k" '[ -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ] || [ -d "$HOME/.local/share/powerlevel10k" ]' ""

echo ""
echo "  [Productivity]"
check_app "Raycast" "/Applications/Raycast.app"
check_app "Alfred" "/Applications/Alfred 5.app"
check_app "Rectangle" "/Applications/Rectangle.app"

echo ""
echo "  [Browsers]"
check_app "Arc" "/Applications/Arc.app"
check_app "Firefox" "/Applications/Firefox.app"
check_app "Chrome" "/Applications/Google Chrome.app"
check_app "Firefox Dev" "/Applications/Firefox Developer Edition.app"

echo ""
echo "  [Communication]"
check_app "Slack" "/Applications/Slack.app"
check_app "Discord" "/Applications/Discord.app"
check_app "Zoom" "/Applications/zoom.us.app"

echo ""
echo "========================================================================"

# Homebrew package count if available
if [ "$BREW_INSTALLED" = true ]; then
    FORMULA_COUNT=$(brew list --formula 2>/dev/null | wc -l | tr -d ' ')
    CASK_COUNT=$(brew list --cask 2>/dev/null | wc -l | tr -d ' ')
    echo "Homebrew packages: $FORMULA_COUNT formulas, $CASK_COUNT casks"
fi

echo ""
echo "Run './scripts/audit-system.py' for full audit with all tasks."
