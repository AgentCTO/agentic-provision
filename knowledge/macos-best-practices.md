# macOS Development Setup Best Practices

## Homebrew

### Installation
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Apple Silicon vs Intel
- Apple Silicon (M1/M2/M3): Homebrew installs to `/opt/homebrew`
- Intel Macs: Homebrew installs to `/usr/local`

After installation on Apple Silicon, add to shell profile:
```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Common Commands
```bash
brew install <package>        # Install CLI tool
brew install --cask <app>     # Install GUI application
brew update                   # Update Homebrew itself
brew upgrade                  # Upgrade all packages
brew list                     # List installed packages
brew search <term>            # Search for packages
brew info <package>           # Get package info
brew cleanup                  # Remove old versions
```

### Brewfile for Reproducible Setup
```ruby
# Brewfile example
tap "homebrew/bundle"
tap "homebrew/cask"

# CLI tools
brew "git"
brew "gh"
brew "jq"
brew "ripgrep"
brew "fzf"

# Applications
cask "visual-studio-code"
cask "docker"
cask "iterm2"
```

Install from Brewfile: `brew bundle install`

---

## Shell Configuration

### Zsh (macOS default since Catalina)

Config files load order:
1. `/etc/zshenv` (system)
2. `~/.zshenv` (always loaded)
3. `~/.zprofile` (login shells)
4. `~/.zshrc` (interactive shells) - **most common to edit**
5. `~/.zlogin` (login shells, after .zshrc)

### PATH Management
```bash
# In ~/.zshrc - add to beginning of PATH
export PATH="$HOME/bin:$PATH"

# Add to end of PATH
export PATH="$PATH:$HOME/bin"
```

### Popular Zsh Enhancements
- **Oh My Zsh**: Framework with themes and plugins
- **Powerlevel10k**: Fast, customizable prompt theme
- **Starship**: Cross-shell prompt (Rust-based, fast)
- **zsh-autosuggestions**: Fish-like suggestions
- **zsh-syntax-highlighting**: Command syntax highlighting

---

## Version Managers

### Node.js - nvm
```bash
# Install
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Usage
nvm install --lts          # Install latest LTS
nvm install 20             # Install Node 20
nvm use 20                 # Switch to Node 20
nvm alias default 20       # Set default version
```

### Node.js - fnm (faster alternative)
```bash
brew install fnm
# Add to ~/.zshrc:
eval "$(fnm env --use-on-cd)"
```

### Python - pyenv
```bash
# Install
brew install pyenv

# Add to ~/.zshrc:
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Usage
pyenv install 3.12.1       # Install version
pyenv global 3.12.1        # Set global default
pyenv local 3.11.0         # Set project-specific version
```

### Ruby - rbenv
```bash
brew install rbenv ruby-build

# Add to ~/.zshrc:
eval "$(rbenv init -)"

# Usage
rbenv install 3.3.0
rbenv global 3.3.0
```

### Multiple Languages - asdf
```bash
brew install asdf

# Add to ~/.zshrc:
. $(brew --prefix asdf)/libexec/asdf.sh

# Usage
asdf plugin add nodejs
asdf plugin add python
asdf install nodejs latest
asdf global nodejs latest
```

### Multiple Languages - mise (modern asdf alternative)
```bash
brew install mise

# Add to ~/.zshrc:
eval "$(mise activate zsh)"

# Usage
mise use node@20
mise use python@3.12
```

---

## Git Configuration

### Basic Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global init.defaultBranch main
```

### Useful Settings
```bash
# Better diff
git config --global core.pager "less -FRX"

# Rebase by default on pull
git config --global pull.rebase true

# Auto-setup remote tracking
git config --global push.autoSetupRemote true

# Helpful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate"
```

### SSH Key Generation
```bash
# Generate key (Ed25519 recommended)
ssh-keygen -t ed25519 -C "your@email.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to agent (macOS Keychain integration)
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Add to ~/.ssh/config:
Host *
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

### GitHub CLI
```bash
brew install gh
gh auth login    # Interactive authentication
gh repo clone owner/repo
gh pr create
gh pr checkout 123
```

---

## Databases

### PostgreSQL
```bash
brew install postgresql@16
brew services start postgresql@16

# Connect
psql postgres
```

### MySQL
```bash
brew install mysql
brew services start mysql

# Secure installation
mysql_secure_installation
```

### Redis
```bash
brew install redis
brew services start redis

# Connect
redis-cli
```

### MongoDB
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Connect
mongosh
```

---

## Docker

### Docker Desktop
```bash
brew install --cask docker
# Then open Docker.app and complete setup
```

### Colima (Docker Desktop alternative, lighter weight)
```bash
brew install colima docker
colima start
```

---

## Editors & IDEs

### VS Code
```bash
brew install --cask visual-studio-code

# Install 'code' CLI command:
# Open VS Code > Cmd+Shift+P > "Shell Command: Install 'code' command"

# Install extensions from CLI:
code --install-extension ms-python.python
```

### Cursor (AI-powered VS Code fork)
```bash
brew install --cask cursor
```

### JetBrains Toolbox (manages all JetBrains IDEs)
```bash
brew install --cask jetbrains-toolbox
```

### Neovim
```bash
brew install neovim

# Popular starter configs:
# - LazyVim: https://www.lazyvim.org/
# - AstroNvim: https://astronvim.com/
# - NvChad: https://nvchad.com/
```

---

## macOS Developer Settings

### Show Hidden Files in Finder
```bash
defaults write com.apple.finder AppleShowAllFiles -bool true
killall Finder
```

### Show Path Bar in Finder
```bash
defaults write com.apple.finder ShowPathbar -bool true
```

### Show Full Path in Finder Title
```bash
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
```

### Faster Key Repeat
```bash
defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15
```

### Disable Press-and-Hold for Accents
```bash
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false
```

---

## Useful CLI Tools

```bash
# Modern alternatives to classic tools
brew install ripgrep      # Better grep (rg)
brew install fd           # Better find
brew install bat          # Better cat with syntax highlighting
brew install eza          # Better ls (formerly exa)
brew install zoxide       # Smarter cd (z)
brew install fzf          # Fuzzy finder
brew install jq           # JSON processor
brew install yq           # YAML processor
brew install htop         # Better top
brew install tldr         # Simplified man pages
brew install httpie       # Better curl for APIs
brew install lazygit      # Terminal UI for git
brew install lazydocker   # Terminal UI for docker
```
