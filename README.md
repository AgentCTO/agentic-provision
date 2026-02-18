# Agentic Provision

![Agentic Provision](agentic-provision.png)

**AI-assisted macOS development environment setup using Claude.**

```bash
curl -fsSL https://raw.githubusercontent.com/AgentCTO/agentic-provision/refs/heads/main/bootstrap.sh | bash
```

## What It Does

The bootstrap script installs everything needed to run the provisioner:

1. Xcode Command Line Tools
2. Homebrew (added to PATH in `~/.zprofile`)
3. Claude Code (`brew install --cask claude-code`)
4. Python environment

Then prints next steps:

```
1. Open a new terminal
2. Authenticate: claude
3. Start the provisioner: provision
```

## How the Provisioner Works

An AI agent asks what you need and sets up your Mac accordingly. No predefined scripts—just describe your development environment and the agent configures it.

```
Agent: What type of development will you be doing?

       A) Full-Stack Web - JavaScript/TypeScript, React, Node.js
       B) DevOps & Infrastructure - Docker, Kubernetes, Terraform
       C) Mobile Development - React Native, Flutter, iOS/Android
       D) Data Science & ML - Python, Jupyter, pandas
       E) Other (describe your needs)

You:   A
```

The agent asks one question at a time, explains trade-offs, then presents a full plan for your approval before touching anything.

## What Can Be Installed

| Category | Examples |
|----------|----------|
| Version Managers | nvm, fnm, pyenv, rbenv, mise |
| Editors | VS Code, Cursor, Neovim, JetBrains IDEs |
| Databases | PostgreSQL, MySQL, MongoDB, Redis, SQLite |
| Containers | Docker Desktop, Colima, Podman |
| Shells | Starship, Oh My Zsh, Powerlevel10k |
| AI Tools | Claude Code, Ollama, Cursor, Windsurf, Aider |
| API Tools | Postman, Bruno, HTTPie, Insomnia |
| Productivity | Raycast, Rectangle, Alfred |
| Cloud CLIs | AWS CLI, gcloud, Azure CLI |
| Security | Trivy, Gitleaks, 1Password CLI |

## Re-running

The script is fully idempotent — safe to run again at any time. Already-installed steps are skipped. Run `provision` directly to add more tools to an existing setup.

## Contributing

1. **Add task manifests** — define new tools in `tasks/core/`
2. **Improve the knowledge base** — better practices, updated tool versions
3. **Report issues** — commands that fail, confusing interactions

## License

MIT

## Acknowledgments

- [Claude Code](https://github.com/anthropics/claude-code) - The AI agent runtime
- [Homebrew](https://brew.sh/) - macOS package management
- [thoughtbot/laptop](https://github.com/thoughtbot/laptop) - Inspiration
