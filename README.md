# Agentic Provision

![Agentic Provision](agentic-provision.png)

**AI-assisted macOS development environment setup using Claude.**

An AI agent guides you through setting up your Mac for development. No predefined scripts—just describe what you need, and the agent configures your system accordingly.

## Why?

Traditional provisioning approaches fail in different ways:

| Approach | Problem |
|----------|---------|
| Dotfiles repos | "Here's my setup, figure out what applies to you" |
| Provisioning scripts | "Install everything, disable what you don't need" |
| Manual setup | "Spend 4 hours researching best practices" |

**Agentic Provision** takes a different approach: an AI agent asks what you need, explains trade-offs, and sets things up correctly.

## How It Works

The agent guides you through a structured conversation:

```
Agent: Welcome to Agentic Provision! I'll help you set up this Mac for development.

       What type of development will you be doing?

       A) Full-Stack Web - JavaScript/TypeScript, React, Node.js, PostgreSQL
       B) DevOps & Infrastructure - Docker, Kubernetes, Terraform, cloud CLIs
       C) Mobile Development - React Native, Flutter, or native iOS/Android
       D) Data Science & ML - Python, Jupyter, pandas, scikit-learn
       E) Other (describe your needs)

You:   A

Agent: Great! Which JavaScript runtime setup do you prefer?

       A) Node.js via nvm - Version management, most widely used
       B) Node.js via fnm - Faster alternative to nvm
       C) Bun - Modern all-in-one runtime and package manager
       D) Not sure - Help me decide
       E) Other

You:   D

Agent: Here's a quick comparison:

       nvm - The standard. Works everywhere, large community.
       fnm - Faster startup, written in Rust. Drop-in replacement.
       Bun - All-in-one runtime, bundler, and package manager. Very fast.

       For most web development, nvm or fnm are safe choices.

       A) nvm - Tried and true
       B) fnm - Faster alternative
       C) Bun - Modern approach
       D) Tell me more

You:   B
```

The conversation continues through tools, editors, databases, AI assistants, and more—then presents a plan for approval.

## Interaction Model

### Agent Speaks First
The agent initiates every interaction with options.

### One Question at a Time
No overwhelming lists of questions. Each response leads to exactly one follow-up.

### Lettered Options
Every question offers 4 choices (A-D) plus a custom option (E):

```
A) First option - Brief description
B) Second option - Brief description
C) Third option - Brief description
D) Not sure / Help me decide
E) Other (describe your needs)
```

You can respond with:
- Just the letter: `A`
- The option name: `nvm`
- Custom text: `I need Node 18 specifically`

### Confirmation Before Action
The agent always shows what it will do and asks for approval:

```
Agent: Here's what I'll set up:

       Package Manager:
         • Homebrew

       Languages:
         • Node.js 20 (LTS) via fnm
         • TypeScript (global)

       Editor:
         • Cursor

       AI Tools:
         • Claude Code

       Productivity:
         • Raycast
         • Rectangle

       Ready to proceed?

       A) Yes, install everything
       B) Yes, but let me review each step
       C) Modify the plan
       D) Start over
```

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/AgentCTO/agentic-provision/refs/heads/main/bootstrap.sh | bash
```

The bootstrap script handles everything: Homebrew, Claude Code, Python environment, API key setup, and offers to launch the provisioner immediately.

## Features

| Feature | Description |
|---------|-------------|
| **Guided setup** | Agent asks questions, you pick options |
| **No assumptions** | Installs only what you choose |
| **Best practices** | Agent knows macOS conventions and common pitfalls |
| **Session persistence** | Resume interrupted setups, expand completed ones |
| **Task manifests** | External YAML definitions for all tools |
| **Step-by-step option** | Review and approve each command individually |
| **Error recovery** | Agent explains failures and offers solutions |

## What Can Be Installed

### Development Stacks
- **Full-Stack Web** - Node.js, TypeScript, React, databases
- **DevOps & Infrastructure** - Docker, Kubernetes, Terraform, cloud CLIs
- **Mobile Development** - React Native, Flutter, Xcode
- **Data Science & ML** - Python, Jupyter, pandas, ML tools

### Tool Categories
| Category | Examples |
|----------|----------|
| Package Managers | Homebrew |
| Version Managers | nvm, fnm, pyenv, rbenv, mise |
| Editors | VS Code, Cursor, Neovim, JetBrains IDEs |
| Databases | PostgreSQL, MySQL, MongoDB, Redis, SQLite |
| Containers | Docker Desktop, Colima, Podman |
| Shells | Starship, Oh My Zsh, Powerlevel10k |
| AI Tools | Claude Code, Ollama, LM Studio, Continue, Cursor |
| API Tools | Postman, Bruno, HTTPie, Insomnia |
| Productivity | Raycast, Rectangle, Alfred |
| Fonts | JetBrains Mono, Fira Code, Nerd Fonts |
| Browsers | Arc, Firefox Developer, Chrome |
| Communication | Slack, Discord |
| Security | Trivy, Gitleaks, 1Password CLI |
| Cloud CLIs | AWS CLI, gcloud, Azure CLI |

## Project Structure

```
agentic-provision/
├── knowledge/                    # Agent knowledge base
│   ├── system-prompt.md          # Agent behavior and interaction rules
│   ├── macos-best-practices.md   # How to set things up correctly
│   ├── common-pitfalls.md        # What to avoid
│   ├── tools-reference.md        # Comprehensive tool installation reference
│   ├── macos-defaults-reference.md  # macOS configuration commands
│   ├── session-schema.md         # Session state JSON structure
│   ├── task-manifest-schema.md   # Task YAML structure
│   └── github-repositories.md    # Curated provisioning repos
├── tasks/
│   ├── core/                     # Built-in task definitions
│   │   ├── package-managers.yaml
│   │   ├── version-managers.yaml
│   │   ├── editors.yaml
│   │   ├── databases.yaml
│   │   ├── containers.yaml
│   │   ├── shells.yaml
│   │   ├── git-setup.yaml
│   │   ├── cli-tools.yaml
│   │   ├── ai-tools.yaml
│   │   ├── api-tools.yaml
│   │   ├── productivity-apps.yaml
│   │   ├── fonts.yaml
│   │   ├── browsers.yaml
│   │   ├── communication.yaml
│   │   ├── security.yaml
│   │   ├── cloud-clis.yaml
│   │   └── macos-defaults.yaml
│   └── profiles/                 # Pre-composed stack profiles
│       ├── fullstack-web.yaml
│       ├── data-science.yaml
│       ├── mobile-dev.yaml
│       └── devops.yaml
├── lib/                          # Python modules
│   ├── provision.py              # Main entry point
│   └── state_manager.py          # Session persistence
├── examples/
│   └── sessions/                 # Example conversation transcripts
├── README.md
└── LICENSE
```

## Session Persistence

Sessions are automatically saved and can be resumed:

```
~/.agentic-provision/
├── sessions/
│   ├── active/      # In-progress sessions
│   ├── completed/   # Finished sessions
│   └── failed/      # Interrupted sessions
└── logs/            # Command execution logs
```

When you restart, the agent detects existing sessions:

```
Agent: I found an active provisioning session from earlier today.

       A) Resume where we left off
       B) Start fresh (abandon previous session)
       C) Show me what was in progress
       D) Exit
```

## Task Manifests

All tool installations are defined in YAML manifests:

```yaml
tasks:
  nvm:
    id: "nvm"
    name: "Node Version Manager"
    description: "Manage multiple Node.js versions"
    category: "version-managers"

    detection:
      check_command: "[ -s \"$HOME/.nvm/nvm.sh\" ]"

    dependencies:
      required: []

    install:
      steps:
        - command: 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash'
          description: "Install nvm"

    post_install:
      shell_integration:
        zsh: |
          export NVM_DIR="$HOME/.nvm"
          [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

### Adding Custom Tasks

Create new tasks in `tasks/core/` or `~/.agentic-provision/tasks/custom/`:

```yaml
tasks:
  my-tool:
    id: "my-tool"
    name: "My Tool"
    description: "Does something useful"

    detection:
      check_command: "command -v my-tool"

    install:
      steps:
        - command: "brew install my-tool"
          description: "Install via Homebrew"
```

## FAQ

**Q: Why an AI agent instead of a script?**

Scripts are static—they can't ask clarifying questions or adapt to your needs. The agent understands context and can explain trade-offs.

**Q: Is this safe?**

The agent shows every command before running it. You approve each action. With "review each step" mode, you confirm every single command.

**Q: What if I choose the wrong option?**

You can always modify the plan or start over. The agent offers these options at every confirmation step.

**Q: Can I expand an existing setup later?**

Yes. The agent detects completed sessions and offers to add more tools without reinstalling what's already there.

**Q: What models work best?**

Claude Sonnet or Opus give the best results for complex setups with nuanced decisions.

## Contributing

Contributions welcome:

1. **Add task manifests** - Define new tools in `tasks/core/`
2. **Improve the knowledge base** - Better practices, updated tool versions
3. **Add example sessions** - Show different setup paths
4. **Report issues** - Commands that fail, confusing interactions

## License

MIT

## Acknowledgments

- [Claude Code](https://github.com/anthropics/claude-code) - The AI agent runtime
- [Homebrew](https://brew.sh/) - macOS package management
- [thoughtbot/laptop](https://github.com/thoughtbot/laptop) - Inspiration
