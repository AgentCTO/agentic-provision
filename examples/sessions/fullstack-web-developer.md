# Example Session: Full-Stack Web Developer

This example demonstrates a complete provisioning session for a full-stack web developer. It follows the question flow defined in `tasks/profiles/fullstack-web.yaml` and shows ideal agent behavior.

---

## Session Start (Phase 0 → Phase 1)

**Agent:**
```
Welcome to Agentic Provision! I'll help you set up this Mac for development.

What type of development will you be doing?

A) Full-Stack Web - JavaScript/TypeScript, React, Node.js, PostgreSQL
B) Backend & APIs - Python with FastAPI or Django, databases
C) Mobile Development - React Native, Flutter, or native iOS/Android
D) Data Science & ML - Python, Jupyter, pandas, scikit-learn
E) Other (describe your needs)
```

**User:** A

---

## Phase 2: Gather Requirements

### Question 1: JavaScript Runtime

**Agent:**
```
Great choice! Let's configure your JavaScript/TypeScript environment.

Which JavaScript runtime setup do you prefer?

A) nvm - Node Version Manager, widely used, easy switching
B) fnm - Fast Node Manager, Rust-based, very quick
C) Direct install - Latest Node.js LTS via Homebrew
D) Not sure - What's the difference?
E) Other
```

**User:** D

**Agent:**
```
Here's a quick comparison:

**nvm** is the most established option. It lets you install multiple Node
versions and switch between them. Great if you work on projects requiring
different Node versions.

**fnm** does the same thing but is written in Rust, making it noticeably
faster. Good if you frequently switch versions or want snappier terminal
startup.

**Direct install** gives you one Node version managed by Homebrew. Simpler,
but harder to switch versions for different projects.

For most developers, **nvm** or **fnm** is recommended.

Which would you prefer?

A) nvm - Node Version Manager, widely used, easy switching
B) fnm - Fast Node Manager, Rust-based, very quick
C) Direct install - Latest Node.js LTS via Homebrew
D) Skip - I'll decide later
E) Other
```

**User:** A

---

### Question 2: Editor

**Agent:**
```
Which code editor do you prefer?

A) VS Code - Free, extensive extensions, industry standard
B) Cursor - AI-powered, built on VS Code, great for productivity
C) Neovim - Terminal-based, highly customizable
D) WebStorm - Full IDE, excellent TypeScript support
E) Other
```

**User:** B

---

### Question 3: Database

**Agent:**
```
Which database will you primarily use?

A) PostgreSQL - Powerful, open-source, great for most web apps
B) MySQL - Popular, widely supported, good performance
C) MongoDB - Document database, flexible schema
D) SQLite - File-based, perfect for local development
E) Other
```

**User:** A

---

### Question 4: Docker

**Agent:**
```
Do you need Docker for containerization?

A) Docker Desktop - Full Docker with GUI, built-in Kubernetes
B) Colima - Free, lightweight Docker runtime (no license needed)
C) OrbStack - Fast, lightweight, great macOS integration
D) No - I don't need containers right now
E) Other
```

**User:** B

---

### Question 5: Shell Customization

**Agent:**
```
Would you like shell customization?

A) Starship - Fast, minimal prompt with git status, node version
B) Oh My Zsh - Popular framework with many plugins
C) Both - Starship prompt with Oh My Zsh plugins
D) None - Keep the default shell
E) Other
```

**User:** A

---

### Question 6: Terminal

**Agent:**
```
Would you like to install a terminal emulator?

A) iTerm2 - Feature-rich, most popular on macOS
B) Warp - Modern, AI-powered, built-in autocomplete
C) Alacritty - GPU-accelerated, minimal, fast
D) None - I'll use the built-in Terminal
E) Other
```

**User:** D

---

### Question 7: Git Setup

**Agent:**
```
Do you need help setting up Git and GitHub?

A) Yes - Configure git and generate SSH keys for GitHub
B) Just git config - Set my name and email
C) No - I already have git configured
D) Skip for now
E) Other
```

**User:** A

**Agent:**
```
I'll need a couple of details for git configuration.

What name should appear in your commits?
```

**User:** Alex Chen

**Agent:**
```
And what email should be associated with your commits?
```

**User:** alex@example.com

---

## Phase 3: Present Plan

**Agent:**
```
Here's what I'll set up:

**Package Manager**
  • Homebrew

**Languages & Runtime**
  • nvm (Node Version Manager)
  • Node.js 20 LTS

**Editor**
  • Cursor

**Database**
  • PostgreSQL 16

**Containers**
  • Colima (Docker runtime)
  • Docker CLI

**Shell**
  • Starship prompt

**Git & GitHub**
  • Git configuration (Alex Chen <alex@example.com>)
  • SSH key generation
  • GitHub CLI (gh)

**CLI Tools** (included by default)
  • ripgrep, fd, bat, fzf, jq, httpie

Ready to proceed?

A) Yes, install everything
B) Yes, but let me review each step
C) Modify the plan
D) Start over
```

**User:** A

---

## Phase 4: Execute

**Agent:**
```
Starting installation...

▶ Checking Homebrew...
```

```
$ command -v brew
```

```
✓ Homebrew already installed (4.2.0)
```

---

**Agent:**
```
▶ Installing nvm...
```

```
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

```
✓ nvm installed

▶ Installing Node.js 20 LTS...
```

```
$ source ~/.nvm/nvm.sh && nvm install 20
```

```
✓ Node.js v20.11.0 installed
```

---

**Agent:**
```
▶ Installing Cursor...
```

```
$ brew install --cask cursor
```

```
✓ Cursor installed
```

---

**Agent:**
```
▶ Installing PostgreSQL...
```

```
$ brew install postgresql@16
```

```
✓ PostgreSQL 16 installed

Starting PostgreSQL service...
```

```
$ brew services start postgresql@16
```

```
✓ PostgreSQL running
```

---

**Agent:**
```
▶ Installing Colima and Docker CLI...
```

```
$ brew install colima docker docker-compose
```

```
✓ Colima and Docker installed

Note: Run `colima start` when you need Docker.
```

---

**Agent:**
```
▶ Installing Starship prompt...
```

```
$ brew install starship
```

```
✓ Starship installed

Adding to shell configuration...
```

```
$ echo 'eval "$(starship init zsh)"' >> ~/.zshrc
```

```
✓ Starship configured
```

---

**Agent:**
```
▶ Configuring Git...
```

```
$ git config --global user.name "Alex Chen"
$ git config --global user.email "alex@example.com"
```

```
✓ Git configured

▶ Generating SSH key...
```

```
$ ssh-keygen -t ed25519 -C "alex@example.com" -f ~/.ssh/id_ed25519 -N ""
```

```
✓ SSH key generated

▶ Installing GitHub CLI...
```

```
$ brew install gh
```

```
✓ GitHub CLI installed
```

---

**Agent:**
```
▶ Installing CLI tools...
```

```
$ brew install ripgrep fd bat fzf jq httpie
```

```
✓ CLI tools installed
```

---

## Phase 5: Completion

**Agent:**
```
✓ Setup complete!

**Installed:**
  • Homebrew (package manager)
  • nvm + Node.js 20.11.0
  • Cursor (editor)
  • PostgreSQL 16 (running)
  • Colima + Docker CLI
  • Starship prompt
  • Git (configured for Alex Chen)
  • SSH key (ready for GitHub)
  • GitHub CLI
  • CLI tools (ripgrep, fd, bat, fzf, jq, httpie)

**Next steps:**

A) Add my SSH key to GitHub (I'll show you how)
B) Start Colima/Docker
C) Open Cursor and install extensions
D) I'm all set, thanks!
```

**User:** A

**Agent:**
```
To add your SSH key to GitHub:

1. Copy your public key:
```

```
$ cat ~/.ssh/id_ed25519.pub | pbcopy
```

```
✓ Public key copied to clipboard

2. Go to: https://github.com/settings/ssh/new
3. Paste the key and give it a name (e.g., "MacBook Pro")
4. Click "Add SSH key"

Or I can open GitHub for you and authenticate via the CLI:
```

```
$ gh auth login
```

```
Would you like me to run this?

A) Yes, authenticate with GitHub CLI
B) No, I'll add the key manually
C) Skip for now
```

**User:** A

**Agent:**
```
$ gh auth login
```

```
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? SSH
? Upload your SSH public key to your GitHub account? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: XXXX-XXXX
Press Enter to open github.com in your browser...
```

```
Follow the prompts in your browser to complete authentication.

Once done, your SSH key will be added to GitHub and you'll be able to
clone repositories using SSH.

A) Done - I've completed authentication
B) Having trouble - help me debug
C) Skip for now
```

**User:** A

**Agent:**
```
✓ GitHub authentication complete!

You're all set. Your Mac is now configured for full-stack web development.

Some useful commands to remember:
  • `nvm use 20` - Switch to Node 20
  • `colima start` - Start Docker runtime
  • `psql` - Connect to PostgreSQL
  • `gh repo clone owner/repo` - Clone a GitHub repo

Happy coding! 🚀
```

---

## Key Behaviors Demonstrated

1. **Single question per response** - Never asks multiple questions at once
2. **Lettered options A-E** - Every question has clear options
3. **"Not sure" handling** - Explains tradeoffs when user selects D
4. **Confirm before execution** - Shows commands before running
5. **Progress indicators** - Uses ▶ for starting, ✓ for success
6. **Minimal explanations** - Brief status updates, not verbose
7. **Helpful next steps** - Offers logical follow-up actions
8. **User agency** - Always gives user control over what happens next
