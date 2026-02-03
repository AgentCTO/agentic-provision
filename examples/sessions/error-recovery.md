# Example Session: Error Recovery & Resume

This example demonstrates how the agent handles errors, session resumption, and expansion of existing setups. These are critical behaviors for a robust provisioning system.

---

## Part 1: Handling Installation Errors

### Scenario: Cask installation fails due to permissions

**Agent:**
```
▶ Installing Docker Desktop...
```

```
$ brew install --cask docker
```

```
✗ Installation failed

Error: Cask 'docker' requires a password to be set in System Preferences.
```

**Agent:**
```
Docker Desktop installation failed because macOS requires password
authentication for this installer.

A) Retry - I'll run with admin privileges (requires password)
B) Try alternative - Install Colima instead (no password needed)
C) Skip - Continue without Docker
D) Show full error output
```

**User:** B

**Agent:**
```
Good choice. Colima is a free, lightweight Docker runtime that doesn't
require special permissions.

▶ Installing Colima...
```

```
$ brew install colima docker docker-compose
```

```
✓ Colima and Docker CLI installed

Note: Run `colima start` to start the Docker runtime.
```

---

### Scenario: Network error during download

**Agent:**
```
▶ Installing nvm...
```

```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

```
✗ Download failed

curl: (7) Failed to connect to raw.githubusercontent.com
```

**Agent:**
```
The download failed - this is usually a network issue.

A) Retry - Try the download again
B) Alternative source - Install via Homebrew instead
C) Skip - Continue without nvm
D) Show connection details
```

**User:** A

**Agent:**
```
Retrying...
```

```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

```
✓ nvm installed successfully
```

---

### Scenario: Homebrew formula not found

**Agent:**
```
▶ Installing custom-tool...
```

```
$ brew install custom-tool
```

```
✗ Installation failed

Error: No formulae or casks found for custom-tool.
```

**Agent:**
```
'custom-tool' isn't available in Homebrew's default repositories.

A) Search for alternatives - Let me look for similar packages
B) Add a tap - If you know which tap has it
C) Manual install - I can help with other installation methods
D) Skip this tool
```

**User:** C

**Agent:**
```
What installation method would you prefer?

A) Download from GitHub releases
B) Build from source
C) Use npm/pip if it's a language package
D) Skip for now
E) Other (tell me where to get it)
```

---

## Part 2: Session Resume (Failed Session)

### Scenario: User returns after a failed session

The launcher detects a failed session and passes the path to the agent.

**Agent:**
```
I found a provisioning session from February 2, 2026 that didn't complete.

Session: Full-Stack Web setup
Stopped at: PostgreSQL installation - "Error: could not create directory"

✓ Completed:
  • Homebrew
  • nvm + Node.js 20
  • Cursor

✗ Failed:
  • PostgreSQL

◯ Remaining:
  • Starship prompt
  • Git configuration

A) Resume and retry PostgreSQL
B) Resume but skip PostgreSQL
C) Start completely fresh
D) Show me what happened
```

**User:** D

**Agent:**
```
Here's the error from the PostgreSQL installation:

$ brew install postgresql@16

Error: Could not create directory /opt/homebrew/var/postgresql@16
Permission denied - /opt/homebrew/var is not writable.

This usually happens when:
1. Homebrew permissions got changed
2. Another process locked the directory
3. Disk permissions issue

A) Fix permissions and retry
B) Skip PostgreSQL, continue with remaining
C) Start fresh
D) Exit and let me fix manually
```

**User:** A

**Agent:**
```
Let me fix the Homebrew permissions first...
```

```
$ sudo chown -R $(whoami) /opt/homebrew/var
```

```
✓ Permissions fixed

Retrying PostgreSQL...
```

```
$ brew install postgresql@16
```

```
✓ PostgreSQL 16 installed

Continuing with remaining tasks...

▶ Installing Starship...
```

---

### Scenario: User chooses to skip failed task

**Agent:**
```
I found a provisioning session that didn't complete.

Session: Data Science setup
Stopped at: Anaconda installation - "Disk space insufficient"

A) Resume and retry Anaconda
B) Resume but skip Anaconda
C) Try Miniconda instead (smaller)
D) Show details
```

**User:** C

**Agent:**
```
Good choice - Miniconda is much smaller (~50MB vs ~3GB).

▶ Installing Miniconda...
```

```
$ brew install --cask miniconda
```

```
✓ Miniconda installed

I'll update the session to reflect this change and continue.
```

---

## Part 3: Session Expansion

### Scenario: User returns to add more tools

The launcher detects a completed session.

**Agent:**
```
Welcome back! I see you set up this Mac on February 2, 2026.

Currently installed:
  • Homebrew
  • nvm + Node.js 20
  • Cursor
  • PostgreSQL 16
  • Starship

A) Add more tools to this setup
B) Start a completely fresh setup
C) Show me everything that's installed
D) Exit
```

**User:** A

**Agent:**
```
What would you like to add?

A) Another programming language (Python, Go, Rust, etc.)
B) Additional database (Redis, MongoDB, MySQL)
C) Container tools (Docker, Kubernetes)
D) DevOps tools (Terraform, Ansible, cloud CLIs)
E) Other (describe what you need)
```

**User:** A

**Agent:**
```
Which language would you like to add?

A) Python - via pyenv for version management
B) Go - via Homebrew
C) Rust - via rustup
D) Multiple - I need several languages
E) Other
```

**User:** A

**Agent:**
```
For Python, I recommend pyenv for version management.

A) pyenv + Python 3.12 (latest)
B) pyenv + Python 3.11 (stable, widely used)
C) pyenv only (I'll install Python versions myself)
D) Not sure - what's the difference?
```

**User:** B

---

**Agent:**
```
Here's what I'll add to your existing setup:

**Languages**
  • pyenv (Python version manager)
  • Python 3.11

This won't affect your existing tools.

Ready to proceed?

A) Yes, install
B) Add more before installing
C) Cancel
```

**User:** A

**Agent:**
```
▶ Installing pyenv...
```

```
$ brew install pyenv
```

```
✓ pyenv installed

Adding to shell configuration...
```

```
$ echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

```
▶ Installing Python 3.11...
```

```
$ pyenv install 3.11.7
$ pyenv global 3.11.7
```

```
✓ Python 3.11.7 installed and set as default

✓ Expansion complete!

Your setup now includes Python. Use `pyenv versions` to see installed
versions and `pyenv install <version>` to add more.

A) Add more tools
B) I'm done
```

---

## Part 4: Handling Edge Cases

### Scenario: Tool already installed (detection)

**Agent:**
```
▶ Checking Homebrew...
```

```
$ command -v brew
/opt/homebrew/bin/brew
```

```
✓ Homebrew already installed (4.2.0) - skipping
```

---

### Scenario: Conflicting tools detected

**Agent:**
```
▶ About to install nvm...

⚠ I noticed you have fnm installed. Both nvm and fnm manage Node.js
versions, and having both can cause conflicts.

A) Keep fnm, skip nvm
B) Remove fnm, install nvm
C) Install both (I know what I'm doing)
D) Help me decide
```

**User:** A

**Agent:**
```
Keeping fnm. I'll configure Node.js installation to use fnm instead.
```

```
$ fnm install 20
$ fnm default 20
```

```
✓ Node.js 20 installed via fnm
```

---

### Scenario: User provides unexpected input

**Agent:**
```
Which editor do you prefer?

A) VS Code - Free, extensive extensions
B) Cursor - AI-powered, built on VS Code
C) Neovim - Terminal-based, highly customizable
D) WebStorm - Full IDE, excellent TypeScript support
E) Other
```

**User:** I use Sublime Text

**Agent:**
```
Got it - Sublime Text is a great choice. I'll add that to your setup.
```

```
$ brew install --cask sublime-text
```

```
✓ Sublime Text installed
```

---

### Scenario: User wants to modify plan

**Agent:**
```
Here's what I'll set up:

**Package Manager**
  • Homebrew

**Languages**
  • nvm + Node.js 20

**Editor**
  • Cursor

Ready to proceed?

A) Yes, install everything
B) Yes, but review each step
C) Modify the plan
D) Start over
```

**User:** C

**Agent:**
```
What would you like to change?

A) Remove something from the plan
B) Add something to the plan
C) Change a specific choice
D) Never mind, proceed as planned
```

**User:** A

**Agent:**
```
What should I remove?

A) Homebrew (not recommended - needed for other tools)
B) nvm + Node.js
C) Cursor
D) Cancel
```

**User:** B

**Agent:**
```
Removed nvm and Node.js from the plan.

Updated plan:

**Package Manager**
  • Homebrew

**Editor**
  • Cursor

Ready to proceed?

A) Yes, install everything
B) Yes, but review each step
C) Modify the plan
D) Start over
```

---

## Key Behaviors Demonstrated

1. **Graceful error handling** - Always offers alternatives, never dead-ends
2. **Clear error explanation** - Brief cause, not verbose stack traces
3. **Retry options** - Allows user to try again before skipping
4. **Session state awareness** - Knows what completed/failed/remains
5. **Conflict detection** - Warns about incompatible tools
6. **Flexible input** - Accepts natural language, not just letters
7. **Plan modification** - Lets users adjust before execution
8. **Expansion workflow** - Seamlessly adds to existing setups
9. **Detection before install** - Skips already-installed tools
