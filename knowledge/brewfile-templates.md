# Brewfile Templates and Examples

Ready-to-use Brewfile templates for different use cases and developer profiles.

---

## Basic Structure

```ruby
# Taps (third-party repositories)
tap "repository/name"

# CLI tools (formulae)
brew "package-name"

# GUI applications (casks)
cask "app-name"

# Mac App Store apps (requires mas)
mas "App Name", id: 123456789

# VS Code extensions
vscode "publisher.extension"
```

---

## Minimal Developer Setup

A lean starting point for any developer.

```ruby
# Brewfile - Minimal Developer Setup

tap "homebrew/bundle"
tap "homebrew/cask"

# Essential CLI
brew "git"
brew "gh"              # GitHub CLI
brew "curl"
brew "wget"

# Modern CLI replacements
brew "ripgrep"         # Better grep
brew "fd"              # Better find
brew "bat"             # Better cat
brew "eza"             # Better ls
brew "fzf"             # Fuzzy finder
brew "jq"              # JSON processor

# Development
brew "node"
brew "python"

# Terminal & Editor
cask "iterm2"
cask "visual-studio-code"

# Browser
cask "firefox"
```

---

## Web Developer Setup

Full-stack web development environment.

```ruby
# Brewfile - Web Developer

tap "homebrew/bundle"
tap "homebrew/cask"
tap "homebrew/cask-fonts"

# === Version Management ===
brew "nvm"             # Node version manager
brew "pyenv"           # Python version manager

# === JavaScript/Node ===
brew "node"
brew "yarn"
brew "pnpm"

# === Package Managers & Build Tools ===
brew "watchman"        # File watcher for React Native

# === Databases ===
brew "postgresql@16"
brew "mysql"
brew "redis"
brew "sqlite"

# === DevOps & Containers ===
brew "docker"
brew "docker-compose"

# === API Development ===
brew "httpie"          # Better curl
brew "jq"              # JSON processor

# === Git & GitHub ===
brew "git"
brew "gh"
brew "git-lfs"
brew "lazygit"         # Terminal UI for git

# === CLI Tools ===
brew "ripgrep"
brew "fd"
brew "bat"
brew "eza"
brew "fzf"
brew "tldr"
brew "tree"

# === Applications ===
cask "visual-studio-code"
cask "iterm2"
cask "docker"
cask "postman"
cask "tableplus"       # Database GUI
cask "figma"
cask "slack"
cask "notion"

# === Browsers ===
cask "firefox"
cask "google-chrome"
cask "arc"

# === Fonts ===
cask "font-fira-code-nerd-font"
cask "font-jetbrains-mono-nerd-font"

# === Mac App Store ===
mas "Xcode", id: 497799835
```

---

## Python Data Science Setup

Data science and machine learning environment.

```ruby
# Brewfile - Python Data Science

tap "homebrew/bundle"
tap "homebrew/cask"

# === Python Environment ===
brew "python@3.12"
brew "pyenv"
brew "pipx"            # Install Python apps in isolation

# === Data Science Tools ===
brew "jupyterlab"

# === Databases ===
brew "postgresql@16"
brew "sqlite"

# === Data Formats ===
brew "jq"              # JSON
brew "yq"              # YAML
brew "csvkit"          # CSV tools

# === Visualization ===
brew "graphviz"

# === Development ===
brew "git"
brew "gh"

# === CLI Tools ===
brew "ripgrep"
brew "fd"
brew "bat"
brew "fzf"
brew "htop"
brew "wget"
brew "curl"

# === Applications ===
cask "visual-studio-code"
cask "pycharm-ce"      # Or pycharm for pro
cask "iterm2"
cask "docker"
cask "tableplus"

# === Notebooks ===
cask "anaconda"        # Alternative: miniconda

# === Communication ===
cask "slack"
cask "zoom"

# === Mac App Store ===
mas "Keynote", id: 409183694
mas "Numbers", id: 409203825
```

---

## DevOps/SRE Setup

Infrastructure and operations focused.

```ruby
# Brewfile - DevOps/SRE

tap "homebrew/bundle"
tap "homebrew/cask"
tap "hashicorp/tap"

# === Containers & Orchestration ===
brew "docker"
brew "docker-compose"
brew "kubectl"
brew "kubectx"         # Switch contexts/namespaces
brew "helm"
brew "k9s"             # Kubernetes TUI
brew "kind"            # Kubernetes in Docker
brew "minikube"

# === Infrastructure as Code ===
brew "hashicorp/tap/terraform"
brew "hashicorp/tap/packer"
brew "ansible"
brew "pulumi"

# === Cloud CLIs ===
brew "awscli"
brew "azure-cli"
brew "google-cloud-sdk"

# === Secrets Management ===
brew "hashicorp/tap/vault"
brew "sops"
brew "age"

# === Networking ===
brew "nmap"
brew "mtr"             # Better traceroute
brew "httpie"
brew "curl"
brew "wget"

# === Monitoring & Logging ===
brew "prometheus"
brew "grafana"

# === Git & VCS ===
brew "git"
brew "gh"
brew "lazygit"
brew "git-secrets"

# === CLI Tools ===
brew "ripgrep"
brew "fd"
brew "bat"
brew "eza"
brew "fzf"
brew "jq"
brew "yq"
brew "htop"
brew "watch"
brew "tree"
brew "tmux"

# === Applications ===
cask "visual-studio-code"
cask "iterm2"
cask "docker"
cask "lens"            # Kubernetes IDE
cask "postman"
cask "wireshark"

# === Communication ===
cask "slack"
cask "zoom"

# === Password Management ===
cask "1password-cli"
```

---

## iOS/macOS Developer Setup

Apple platform development environment.

```ruby
# Brewfile - iOS/macOS Developer

tap "homebrew/bundle"
tap "homebrew/cask"

# === Swift/iOS Tools ===
brew "swiftlint"
brew "swiftformat"
brew "xcbeautify"      # Prettier xcodebuild output
brew "xcode-build-times"
brew "cocoapods"
brew "carthage"

# === Version Management ===
brew "rbenv"           # Ruby for CocoaPods
brew "ruby-build"

# === CLI Tools ===
brew "git"
brew "gh"
brew "lazygit"
brew "ripgrep"
brew "fd"
brew "bat"
brew "fzf"
brew "jq"
brew "tree"

# === Networking ===
brew "httpie"
brew "charles-proxy"

# === Applications ===
cask "xcode"           # Also install via mas below
cask "visual-studio-code"
cask "sublime-text"
cask "iterm2"
cask "sf-symbols"      # Apple SF Symbols
cask "dash"            # Documentation browser
cask "proxyman"        # HTTP debugging proxy
cask "figma"
cask "sketch"

# === Testing ===
cask "charles"
cask "postman"

# === Design ===
cask "figma"
cask "zeplin"

# === Browsers (for testing) ===
cask "firefox"
cask "google-chrome"
cask "safari-technology-preview"

# === Mac App Store ===
mas "Xcode", id: 497799835
mas "Developer", id: 640199958
mas "TestFlight", id: 899247664
mas "Transporter", id: 1450874784
mas "Apple Configurator 2", id: 1037126344
```

---

## Productivity & Creative Setup

General productivity with creative tools.

```ruby
# Brewfile - Productivity & Creative

tap "homebrew/bundle"
tap "homebrew/cask"
tap "homebrew/cask-fonts"

# === CLI Essentials ===
brew "git"
brew "ripgrep"
brew "fd"
brew "bat"
brew "fzf"
brew "tree"

# === Productivity Apps ===
cask "raycast"         # Spotlight replacement
cask "1password"
cask "notion"
cask "obsidian"
cask "todoist"
cask "fantastical"     # Calendar

# === Communication ===
cask "slack"
cask "discord"
cask "zoom"
cask "signal"

# === Browsers ===
cask "arc"
cask "firefox"
cask "google-chrome"

# === Writing ===
cask "ia-writer"
cask "grammarly-desktop"

# === Creative ===
cask "figma"
cask "canva"
cask "adobe-creative-cloud"

# === Media ===
cask "spotify"
cask "vlc"
cask "iina"            # Modern video player
cask "handbrake"

# === Utilities ===
cask "cleanmymac"
cask "bartender"       # Menu bar management
cask "rectangle"       # Window management
cask "monitorcontrol"  # External display control
cask "karabiner-elements"  # Keyboard customization

# === Screenshot & Recording ===
cask "cleanshot"
cask "loom"

# === Fonts ===
cask "font-inter"
cask "font-fira-code-nerd-font"

# === Mac App Store ===
mas "Magnet", id: 441258766
mas "Things 3", id: 904280696
mas "Bear", id: 1091189122
mas "Craft", id: 1487937127
mas "Keynote", id: 409183694
mas "Pages", id: 409201541
mas "Numbers", id: 409203825
```

---

## Security Researcher Setup

Security analysis and research tools.

```ruby
# Brewfile - Security Research

tap "homebrew/bundle"
tap "homebrew/cask"

# === Network Analysis ===
brew "nmap"
brew "masscan"
brew "tcpdump"
brew "mtr"
brew "iperf3"
brew "httpie"

# === Cryptography ===
brew "gnupg"
brew "openssl"
brew "age"
brew "sops"

# === Forensics & Analysis ===
brew "binwalk"
brew "exiftool"
brew "foremost"
brew "volatility"
brew "yara"

# === Password & Hash Tools ===
brew "john"            # John the Ripper
brew "hashcat"

# === Web Security ===
brew "nikto"
brew "sqlmap"
brew "wpscan"

# === Reverse Engineering ===
brew "radare2"
cask "ghidra"
cask "hopper-disassembler"

# === CLI Essentials ===
brew "git"
brew "gh"
brew "ripgrep"
brew "fd"
brew "bat"
brew "fzf"
brew "jq"
brew "xxd"
brew "hexyl"           # Hex viewer

# === Python (for tools) ===
brew "python"
brew "pipx"

# === Applications ===
cask "visual-studio-code"
cask "iterm2"
cask "wireshark"
cask "burp-suite"
cask "charles"
cask "proxyman"

# === VMs & Containers ===
cask "docker"
cask "virtualbox"
cask "utm"             # QEMU-based VM

# === Password Management ===
cask "1password"
cask "bitwarden"
```

---

## Conditional Brewfile (Advanced)

Using Ruby logic for machine-specific configurations.

```ruby
# Brewfile - Conditional Setup

tap "homebrew/bundle"
tap "homebrew/cask"

# === Always Install ===
brew "git"
brew "gh"
brew "ripgrep"
brew "fd"
brew "bat"
brew "fzf"
brew "jq"

cask "iterm2"
cask "visual-studio-code"

# === Work Machine ===
if ENV["WORK_MACHINE"] || File.exist?(File.expand_path("~/.work-machine"))
  cask "slack"
  cask "zoom"
  cask "microsoft-teams"
  cask "1password"

  # Work-specific tools
  brew "awscli"
  brew "kubectl"
end

# === Personal Machine ===
if ENV["PERSONAL_MACHINE"] || File.exist?(File.expand_path("~/.personal-machine"))
  cask "spotify"
  cask "discord"
  cask "steam"
  cask "vlc"
end

# === M1/M2/M3 Mac specific ===
if `uname -m`.strip == "arm64"
  # ARM-native apps
  cask "utm"           # ARM-native VM
end

# === Only if Docker not already installed ===
unless File.exist?("/Applications/Docker.app")
  cask "docker"
end

# === Development profile ===
if ENV["DEV_PROFILE"] == "web"
  brew "node"
  brew "yarn"
  brew "postgresql@16"
elsif ENV["DEV_PROFILE"] == "python"
  brew "python"
  brew "pyenv"
  brew "pipx"
elsif ENV["DEV_PROFILE"] == "mobile"
  brew "cocoapods"
  brew "fastlane"
end
```

**Usage**:
```bash
# Work machine
WORK_MACHINE=1 brew bundle

# Personal with web dev profile
PERSONAL_MACHINE=1 DEV_PROFILE=web brew bundle

# Or use marker files
touch ~/.work-machine
brew bundle
```

---

## Tips & Best Practices

### Organizing Your Brewfile
```ruby
# Group by category with comments
# === Section Name ===
brew "tool1"
brew "tool2"
```

### Generate from Existing Setup
```bash
# Export current installations
brew bundle dump --describe --force

# Include mas apps
brew bundle dump --describe --mas --force
```

### Cleanup Unused Packages
```bash
# See what would be removed
brew bundle cleanup

# Actually remove
brew bundle cleanup --force
```

### Version Pinning (when needed)
```bash
# Pin to prevent upgrades
brew pin postgresql@16

# Unpin
brew unpin postgresql@16
```

### Global vs Project Brewfiles
```bash
# Install from global
brew bundle install --global  # Uses ~/.Brewfile

# Install from project
brew bundle install --file=./Brewfile

# Install from URL
brew bundle install --file=https://example.com/Brewfile
```

---

## Quick Start Templates

Copy the appropriate template above and save as `Brewfile`, then run:

```bash
brew bundle install
```

For a fresh Mac, first install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/opt/homebrew/bin/brew shellenv)"
brew bundle install
```
