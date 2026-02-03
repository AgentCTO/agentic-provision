# Mac Provisioning Tools Reference

A comprehensive reference of tools and utilities for automating macOS setup and provisioning.

---

## Package Management

### Homebrew
**The essential package manager for macOS.**

- **Repository**: https://github.com/Homebrew/brew
- **Stars**: 40,000+
- **Documentation**: https://brew.sh

**Key Commands**:
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Core commands
brew install <package>        # CLI tools
brew install --cask <app>     # GUI applications
brew update                   # Update Homebrew
brew upgrade                  # Upgrade all packages
brew bundle                   # Install from Brewfile
brew bundle dump              # Export installed packages to Brewfile
```

**Installation Paths**:
- Apple Silicon (M1/M2/M3/M4): `/opt/homebrew`
- Intel Macs: `/usr/local`

---

### Homebrew Bundle
**Declarative package management via Brewfile.**

- **Documentation**: https://docs.brew.sh/Brew-Bundle-and-Brewfile

**Brewfile Syntax**:
```ruby
tap "homebrew/bundle"
tap "homebrew/cask"

# CLI tools
brew "git"
brew "node"
brew "python"

# GUI applications
cask "visual-studio-code"
cask "docker"
cask "iterm2"

# Mac App Store apps (requires mas)
mas "Xcode", id: 497799835
mas "1Password", id: 1333542190
```

**Key Commands**:
```bash
brew bundle install              # Install from Brewfile
brew bundle dump                 # Generate Brewfile from installed packages
brew bundle dump --global        # Generate ~/.Brewfile
brew bundle cleanup --force      # Remove packages not in Brewfile
brew bundle check                # Check if all dependencies are satisfied
```

---

### mas-cli (Mac App Store CLI)
**Command-line interface for the Mac App Store.**

- **Repository**: https://github.com/mas-cli/mas
- **Stars**: 12,000+
- **Minimum macOS**: 13 (Ventura)

**Installation**:
```bash
brew install mas
```

**Key Commands**:
```bash
mas list                    # List installed App Store apps
mas search <term>           # Search for apps
mas install <app-id>        # Install app (requires prior purchase)
mas get <app-id>            # Install free apps
mas upgrade                 # Upgrade all outdated apps
mas outdated                # List apps with updates
mas lucky <term>            # Install first search result
```

**Note**: As of mas 4.0.0+, root privileges required for install/update operations due to macOS security changes.

---

## Dotfile Management

### chezmoi
**Secure, multi-machine dotfile management.**

- **Repository**: https://github.com/twpayne/chezmoi
- **Stars**: 17,800+
- **Documentation**: https://chezmoi.io

**Key Features**:
- Templates for machine-specific configurations
- Built-in encryption (GPG, age)
- Password manager integration (1Password, Bitwarden, etc.)
- Diff before applying changes

**Installation**:
```bash
brew install chezmoi
```

**Basic Usage**:
```bash
chezmoi init                    # Initialize
chezmoi add ~/.zshrc            # Add a dotfile
chezmoi edit ~/.zshrc           # Edit managed file
chezmoi diff                    # Show pending changes
chezmoi apply                   # Apply changes
chezmoi update                  # Pull and apply from repo
```

---

### yadm (Yet Another Dotfiles Manager)
**Git-based dotfile management with encryption.**

- **Repository**: https://github.com/yadm-dev/yadm
- **Stars**: 6,100+
- **Documentation**: https://yadm.io

**Key Features**:
- Uses native Git (no learning curve)
- System-specific alternate files
- Multiple encryption backends (GnuPG, OpenSSL, transcrypt, git-crypt)
- Bootstrap scripting

**Installation**:
```bash
brew install yadm
```

**Basic Usage**:
```bash
yadm init                       # Initialize repository
yadm add ~/.zshrc               # Track a file
yadm commit -m "Add zshrc"      # Commit changes
yadm push                       # Push to remote
yadm clone <url>                # Clone existing dotfiles
```

**Alternate Files** (OS-specific configs):
```
~/.config/git/config##os.Darwin    # macOS
~/.config/git/config##os.Linux     # Linux
~/.config/git/config##class.work   # Work machines
```

**Encryption**:
```bash
echo ".ssh/id_rsa" >> ~/.config/yadm/encrypt
yadm encrypt
yadm decrypt
```

---

### Mackup
**Application settings backup and sync.**

- **Repository**: https://github.com/lra/mackup
- **Stars**: 15,100+
- **Supported Apps**: 400+

**Key Features**:
- Backs up application preferences
- Syncs across machines via cloud storage
- Supports Dropbox, Google Drive, iCloud, or any folder

**Installation**:
```bash
brew install mackup
```

**Usage**:
```bash
mackup backup                   # Backup settings
mackup restore                  # Restore on new machine
mackup list                     # List supported applications
mackup uninstall                # Revert to original locations
```

**Important**: Use `copy` mode on macOS Sonoma (14+) - symlink mode breaks preferences.

**Configuration** (`~/.mackup.cfg`):
```ini
[storage]
engine = icloud

[applications_to_sync]
sublime-text-3
vscode

[applications_to_ignore]
spotify
```

---

## Automation Frameworks

### Ansible (geerlingguy/mac-dev-playbook)
**Infrastructure-as-code Mac provisioning.**

- **Repository**: https://github.com/geerlingguy/mac-dev-playbook
- **Stars**: 6,800+
- **Ansible Collection**: https://github.com/geerlingguy/ansible-collection-mac

**Key Features**:
- Declarative configuration
- Idempotent execution
- Role-based organization
- Continuous testing on GitHub Actions

**Installation**:
```bash
# Install Ansible
pip3 install ansible

# Clone playbook
git clone https://github.com/geerlingguy/mac-dev-playbook.git
cd mac-dev-playbook

# Install dependencies
ansible-galaxy install -r requirements.yml

# Run playbook
ansible-playbook main.yml --ask-become-pass
```

**Ansible Collection Roles**:
- `geerlingguy.mac.homebrew` - Package management
- `geerlingguy.mac.mas` - Mac App Store apps
- `geerlingguy.mac.dock` - Dock configuration

**Tag-based Execution**:
```bash
ansible-playbook main.yml -K --tags "homebrew,mas"
ansible-playbook main.yml -K --tags "dotfiles"
```

---

### nix-darwin
**Declarative macOS system configuration.**

- **Repository**: https://github.com/nix-darwin/nix-darwin
- **Stars**: 5,000+
- **Documentation**: Built-in via `darwin-help`

**Key Features**:
- Declarative system configuration
- Atomic upgrades and rollbacks
- Reproducible builds
- Access to 80,000+ Nix packages

**Installation** (Flakes method):
```bash
# Install Nix
curl -L https://nixos.org/nix/install | sh

# Create configuration
mkdir -p /etc/nix-darwin
# Create flake.nix with your configuration

# Build and switch
sudo nix run nix-darwin/master#darwin-rebuild -- switch
```

**Example Configuration**:
```nix
{ config, pkgs, ... }:
{
  environment.systemPackages = with pkgs; [
    git
    vim
    ripgrep
  ];

  homebrew = {
    enable = true;
    casks = [ "firefox" "visual-studio-code" ];
  };

  system.defaults.dock.autohide = true;
}
```

---

### zero.sh
**Minimal bootstrapping tool.**

- **Repository**: https://github.com/zero-sh/zero.sh
- **Stars**: 320+

**Key Features**:
- Radically simple approach
- Pre-defined directory structure
- No configuration files needed
- Workspace support for multiple machines

**Installation**:
```bash
brew install zero-sh/tap/zero
```

**Directory Structure**:
```
~/.dotfiles/
├── Brewfile              # Homebrew packages
├── defaults.yaml         # macOS preferences
├── symlinks/             # Files to symlink
│   ├── .zshrc
│   └── .gitconfig
└── run/
    ├── before/           # Pre-setup scripts
    └── after/            # Post-setup scripts
```

**Usage**:
```bash
zero setup                      # Run complete setup
zero update                     # Update packages
```

---

## Shell Script Frameworks

### mathiasbynens/dotfiles
**The gold standard for macOS dotfiles.**

- **Repository**: https://github.com/mathiasbynens/dotfiles
- **Stars**: 31,200+
- **License**: MIT

**Key Features**:
- Comprehensive `.macos` script for system defaults
- Sensible shell configurations
- Extensible via `~/.extra` and `~/.path`

**Installation**:
```bash
git clone https://github.com/mathiasbynens/dotfiles.git
cd dotfiles
source bootstrap.sh
```

**Apply macOS Defaults**:
```bash
./.macos
```

---

### donnemartin/dev-setup
**Modular development environment setup.**

- **Repository**: https://github.com/donnemartin/dev-setup
- **Stars**: 6,300+

**Available Scripts**:
| Script | Purpose |
|--------|---------|
| `bootstrap.sh` | Sync dotfiles |
| `osxprep.sh` | Install Xcode CLI tools |
| `brew.sh` | Install Homebrew packages |
| `osx.sh` | Configure macOS defaults |
| `pydata.sh` | Python data science setup |
| `aws.sh` | AWS/Spark/Hadoop tools |
| `datastores.sh` | MySQL, MongoDB, Redis |
| `web.sh` | Node.js, JavaScript tools |
| `android.sh` | Android development |

**Usage**:
```bash
git clone https://github.com/donnemartin/dev-setup.git
cd dev-setup
./.dots bootstrap osxprep brew osx
```

---

### bkuhlmann/mac_os
**Comprehensive macOS automation.**

- **Repository**: https://github.com/bkuhlmann/mac_os
- **Stars**: 505+

**Features**:
- Boot disk creation
- Xcode CLI tools installation
- Homebrew management
- App Store software
- Dotfiles configuration
- Package managers (npm, gems, crates)

**Installation**:
```bash
git clone https://github.com/bkuhlmann/mac_os.git
cd mac_os
git checkout 22.1.0
bin/run
```

---

## macOS Defaults Management

### SixArm/macos-defaults
**Curated macOS defaults commands.**

- **Repository**: https://github.com/SixArm/macos-defaults

**Common Defaults**:
```bash
# Show all filename extensions
defaults write NSGlobalDomain AppleShowAllExtensions -bool true

# Faster key repeat
defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15

# Show hidden files in Finder
defaults write com.apple.finder AppleShowAllFiles -bool true

# Disable press-and-hold for keys
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false

# Show path bar in Finder
defaults write com.apple.finder ShowPathbar -bool true

# Apply changes
killall Finder
killall Dock
```

---

### clintmod/macprefs
**Backup and restore Mac preferences.**

- **Repository**: https://github.com/clintmod/macprefs

**Usage**:
```bash
# Backup preferences
./backup.sh

# Restore preferences
./restore.sh
```

**Note**: Requires Full Disk Access in System Preferences for Terminal.

---

## Enterprise/MDM Tools

### Setup Your Mac
**Jamf Pro integration for end-user self-service.**

- **Repository**: https://github.com/setup-your-mac/Setup-Your-Mac
- **Documentation**: Comprehensive wiki available

**Key Features**:
- swiftDialog-based UI
- Jamf Pro Policy Custom Events
- Zero-touch deployment support
- Automated Device Enrollment integration

---

### munki/macadmin-scripts
**macOS admin utilities.**

- **Repository**: https://github.com/munki/macadmin-scripts
- **Stars**: 2,400+

**Key Scripts**:
- `installinstallmacos.py` - Create bootable macOS installers
- `getmacosipsws.py` - Download macOS IPSW files

**Usage**:
```bash
python3 ./installinstallmacos.py --help
```

---

## Quick Reference: Tool Selection Guide

| Need | Recommended Tool |
|------|------------------|
| Simple package management | Homebrew + Brewfile |
| Multi-machine dotfiles | chezmoi |
| Git-native dotfiles | yadm |
| App settings sync | Mackup |
| Full automation | Ansible (mac-dev-playbook) |
| Declarative system config | nix-darwin |
| Minimal bootstrapping | zero.sh |
| macOS defaults | mathiasbynens/dotfiles `.macos` |
| Enterprise/MDM | Setup Your Mac |
