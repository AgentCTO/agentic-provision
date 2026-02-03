# Common Pitfalls to Avoid

## Installation Issues

### Don't Use System Python
macOS includes Python, but it's for system use. Never rely on `/usr/bin/python3`.

**Problem:**
```bash
# System Python - don't use for development
/usr/bin/python3 -m pip install package  # May require sudo, pollutes system
```

**Solution:**
```bash
# Use pyenv or Homebrew Python
brew install pyenv
pyenv install 3.12
pyenv global 3.12
```

---

### Don't Use `sudo` with Homebrew
Homebrew is designed to work without root access.

**Problem:**
```bash
sudo brew install node  # WRONG - creates permission issues
```

**Solution:**
```bash
brew install node  # Correct - no sudo needed
```

If Homebrew asks for sudo, something is misconfigured. Fix permissions:
```bash
sudo chown -R $(whoami) $(brew --prefix)/*
```

---

### Don't Install Node/Python Globally via Homebrew for Development
Using `brew install node` or `brew install python` works but lacks version management.

**Problem:**
```bash
brew install node  # Only one version, can't switch
```

**Solution:**
```bash
# Use a version manager
brew install nvm   # Then: nvm install 20, nvm install 18
brew install pyenv # Then: pyenv install 3.12, pyenv install 3.11
```

---

### Don't Forget to Source Shell Config After Changes

**Problem:**
```bash
# Add to ~/.zshrc
export PATH="$HOME/bin:$PATH"
# Then wonder why it doesn't work
```

**Solution:**
```bash
# Either restart terminal or:
source ~/.zshrc
```

---

## Shell Configuration Issues

### Don't Overwrite ~/.zshrc
Always append, never overwrite.

**Problem:**
```bash
echo 'export PATH="$HOME/bin:$PATH"' > ~/.zshrc  # DESTROYS existing config
```

**Solution:**
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc  # APPENDS to config
```

---

### PATH Order Matters

**Problem:**
```bash
# Homebrew Python not being used
which python3  # Shows /usr/bin/python3 instead of Homebrew's
```

**Solution:**
Ensure Homebrew's path comes BEFORE system paths:
```bash
# In ~/.zshrc - Homebrew path should be first
export PATH="/opt/homebrew/bin:$PATH"
```

---

### Don't Mix Package Managers for the Same Tool

**Problem:**
```bash
brew install node
npm install -g n  # Another Node version manager - conflicts!
```

**Solution:**
Pick one approach and stick with it:
- Homebrew for simple, single-version needs
- nvm/fnm for multiple Node versions
- Never mix

---

## Git Issues

### Don't Commit Secrets

**Problem:**
```bash
git add .env
git commit -m "Add config"  # API keys now in git history forever
```

**Solution:**
```bash
# Create .gitignore FIRST
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
echo "credentials.json" >> .gitignore
```

---

### Don't Use HTTPS When You Have SSH Keys

**Problem:**
```bash
git clone https://github.com/user/repo.git
# Now you have to enter credentials every time
```

**Solution:**
```bash
# Set up SSH key first, then:
git clone git@github.com:user/repo.git

# Or switch existing repos:
git remote set-url origin git@github.com:user/repo.git
```

---

## Docker Issues

### Don't Forget Docker Desktop License

Docker Desktop requires a paid license for companies with >250 employees or >$10M revenue.

**Alternatives for those cases:**
- Colima (free, open source)
- Podman
- OrbStack (paid, but often cheaper)

---

### Don't Run Containers as Root

**Problem:**
```dockerfile
# Dockerfile
FROM node:20
# Running as root by default
```

**Solution:**
```dockerfile
FROM node:20
USER node
WORKDIR /home/node/app
```

---

## Apple Silicon (M1/M2/M3) Issues

### Watch for x86 vs ARM Binaries

Some tools may not have native ARM builds yet.

**Check architecture:**
```bash
file $(which some-binary)
# Should show "arm64" not "x86_64"
```

**Force x86 via Rosetta (if needed):**
```bash
arch -x86_64 brew install some-package
```

---

### Docker Image Compatibility

**Problem:**
```bash
docker pull some-image  # Might be x86 only, runs slowly via emulation
```

**Solution:**
Look for multi-arch images or ARM-specific tags:
```bash
docker pull --platform linux/arm64 some-image
```

---

## Security Issues

### Don't Pipe Curl to Bash Without Checking

**Risky:**
```bash
curl -fsSL https://some-unknown-site.com/install.sh | bash
```

**Safer:**
```bash
# Download first, inspect, then run
curl -fsSL https://some-site.com/install.sh -o install.sh
less install.sh  # Review it
bash install.sh
```

For well-known, trusted sources (Homebrew, nvm, etc.), pipe-to-bash is generally accepted.

---

### Don't Store Secrets in Shell Config

**Problem:**
```bash
# In ~/.zshrc
export AWS_SECRET_ACCESS_KEY="actual-secret-here"  # Visible in plain text
```

**Solution:**
Use a secrets manager or environment-specific files:
```bash
# Use macOS Keychain
security add-generic-password -a "$USER" -s "AWS_SECRET" -w "actual-secret"

# Or use a tool like direnv with .envrc (gitignored)
# Or use 1Password CLI, aws-vault, etc.
```

---

## Performance Issues

### Don't Load Too Much in Shell Startup

**Problem:**
```bash
# ~/.zshrc
eval "$(pyenv init -)"
eval "$(rbenv init -)"
eval "$(nvm init)"  # NVM is notoriously slow
# Shell takes 2+ seconds to start
```

**Solution:**
- Use lazy loading where possible
- Consider faster alternatives (fnm instead of nvm)
- Use mise instead of multiple version managers

```bash
# Lazy load NVM
nvm() {
    unset -f nvm
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    nvm "$@"
}
```

---

## Database Issues

### Don't Forget to Start Services

**Problem:**
```bash
brew install postgresql@16
psql postgres  # Error: connection refused
```

**Solution:**
```bash
brew services start postgresql@16
# Or for one-time:
pg_ctl -D /opt/homebrew/var/postgresql@16 start
```

---

### Don't Use Default Credentials in Development

Even locally, practice good habits:
```bash
# Create a dedicated database user
createuser --interactive myapp_dev
createdb -O myapp_dev myapp_development
```
