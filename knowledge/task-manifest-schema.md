# Task Manifest Schema

This document defines the YAML schema for task manifests used by the provisioning agent.

## Overview

Task manifests define:
- **What** tools/software can be installed
- **How** to detect if they're already installed
- **How** to install them
- **What** dependencies they have
- **What** shell configuration they need

The agent reads these manifests as reference material when executing provisioning.

## File Locations

```
~/.agentic-provision/tasks/
├── core/           # Built-in task definitions (read-only)
│   ├── package-managers.yaml
│   ├── version-managers.yaml
│   ├── editors.yaml
│   ├── databases.yaml
│   ├── containers.yaml
│   ├── shells.yaml
│   ├── git-setup.yaml
│   └── cli-tools.yaml
├── profiles/       # Pre-composed development stacks (read-only)
│   ├── fullstack-web.yaml
│   ├── data-science.yaml
│   ├── mobile-dev.yaml
│   └── devops.yaml
└── custom/         # User/agent-created tasks (writable)
    └── *.yaml
```

---

## Task Definition Schema

### Complete Structure

```yaml
# File: tasks/core/<category>.yaml

metadata:
  category: "string"
  description: "string"
  author: "string"
  version: "string"
  created: "YYYY-MM-DD"
  updated: "YYYY-MM-DD"

tasks:
  <task_id>:
    id: "string"
    name: "string"
    description: "string"
    category: "string"
    tags: ["array", "of", "strings"]

    detection:
      check_command: "string"
      version_command: "string"
      installed_indicator: "string (file path)"

    dependencies:
      required: ["array", "of", "task_ids"]
      one_of: ["array", "of", "task_ids"]
      optional: ["array", "of", "task_ids"]

    install:
      steps:
        - name: "string"
          command: "string"
          description: "string"
          idempotent: boolean
          requires_sudo: boolean
          shell_config: boolean
      variants:
        <variant_name>:
          steps:
            - name: "string"
              command: "string"
              description: "string"

    shell_integration:
      zsh: "string (multiline)"
      bash: "string (multiline)"

    post_install:
      - task: "string (task_id)"
        condition: "always | user_choice | if_missing"
        prompt: "string (optional)"

    verification:
      command: "string"
      expected_pattern: "string (regex)"
      expected_output: "string (exact match)"

    conflicts_with: ["array", "of", "task_ids"]

    options:
      - id: "string"
        prompt: "string"
        default: "string | number | boolean"
        type: "string | number | boolean | choice"
        choices: ["array", "if", "type=choice"]

    notes: "string (multiline, shown to user)"
    docs_url: "string (URL)"
```

---

## Field Reference

### metadata

File-level metadata about the manifest.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string | Yes | Category identifier (e.g., "version-managers") |
| `description` | string | Yes | Human-readable description of this category |
| `author` | string | No | Who created/maintains this manifest |
| `version` | string | No | Manifest version for tracking changes |
| `created` | date | No | Creation date (YYYY-MM-DD) |
| `updated` | date | No | Last update date |

### tasks.<task_id>

Each task is keyed by a unique identifier.

#### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Must match the key |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | Brief description (one sentence) |
| `category` | string | Yes | Category this task belongs to |
| `tags` | array | No | Keywords for searching/filtering |

#### detection

How to check if this tool is already installed.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `check_command` | string | Yes* | Command that succeeds if installed |
| `version_command` | string | No | Command to get version |
| `installed_indicator` | string | Yes* | File path that exists if installed |

*At least one of `check_command` or `installed_indicator` is required.

**Examples**:
```yaml
detection:
  check_command: "command -v node"
  version_command: "node --version"

# Or for apps without CLI:
detection:
  installed_indicator: "/Applications/Docker.app"
```

#### dependencies

Other tasks that must be present.

| Field | Type | Description |
|-------|------|-------------|
| `required` | array | All must be installed first |
| `one_of` | array | At least one must be installed |
| `optional` | array | Enhanced functionality if present |

**Example**:
```yaml
dependencies:
  required: ["homebrew"]
  one_of: ["nvm", "fnm"]  # Node.js needs a version manager
```

#### install

Installation commands.

**Simple form** (single installation path):
```yaml
install:
  steps:
    - name: "Install via Homebrew"
      command: "brew install ripgrep"
      description: "Install ripgrep for fast searching"
      idempotent: true
```

**Variant form** (multiple installation paths based on dependencies):
```yaml
install:
  variants:
    nvm:
      steps:
        - name: "Install Node LTS via nvm"
          command: "source ~/.nvm/nvm.sh && nvm install --lts"
    fnm:
      steps:
        - name: "Install Node LTS via fnm"
          command: "fnm install --lts"
```

**Step fields**:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | Required | Step identifier |
| `command` | string | Required | Shell command to execute |
| `description` | string | Required | What this command does |
| `idempotent` | boolean | false | Safe to run multiple times |
| `requires_sudo` | boolean | false | Needs elevated privileges |
| `shell_config` | boolean | false | Modifies shell config files |

#### shell_integration

Lines to add to shell configuration files.

```yaml
shell_integration:
  zsh: |
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  bash: |
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

The agent should:
1. Check if these lines already exist
2. Add them if missing
3. Prompt user before modifying shell configs

#### post_install

Tasks to suggest or run after this task completes.

```yaml
post_install:
  - task: "node-lts"
    condition: "user_choice"
    prompt: "Install Node.js LTS?"
  - task: "npm-global-packages"
    condition: "if_missing"
```

**Conditions**:
- `always` - Always run this task
- `user_choice` - Ask user if they want it
- `if_missing` - Run only if not already installed

#### verification

How to confirm successful installation.

```yaml
verification:
  command: "node --version"
  expected_pattern: "^v\\d+\\.\\d+\\.\\d+$"

# Or exact match:
verification:
  command: "which brew"
  expected_output: "/opt/homebrew/bin/brew"
```

#### conflicts_with

Tasks that cannot coexist (mutually exclusive).

```yaml
conflicts_with: ["fnm", "volta", "asdf-nodejs"]
```

The agent should:
1. Check for conflicts before installation
2. Warn user if conflict detected
3. Offer to remove conflicting tool or skip

#### options

Configurable options for the task.

```yaml
options:
  - id: "version"
    prompt: "Which version to install?"
    default: "latest"
    type: "string"

  - id: "node_version"
    prompt: "Node.js version"
    type: "choice"
    choices: ["20", "18", "16"]
    default: "20"
```

#### notes

Important information to show the user.

```yaml
notes: |
  NVM is the most widely-used Node version manager, but it can slow
  down shell startup. Consider fnm if you notice slow terminal loading.
```

---

## Profile Definition Schema

Profiles compose tasks into development stacks.

### Complete Structure

```yaml
# File: tasks/profiles/<profile>.yaml

metadata:
  id: "string"
  name: "string"
  description: "string"
  version: "string"

selection_prompt:
  letter: "A | B | C | D"
  text: "string (shown in stack selection)"

required_tasks:
  - "task_id"

question_flow:
  - id: "string"
    question: "string"
    options:
      - letter: "A | B | C | D"
        text: "string"
        tasks: ["array", "of", "task_ids"]
        user_data_required: ["array", "of", "data_keys"]
      - letter: "D"
        text: "Not sure - Help me decide"
        action: "explain"

default_cli_tools:
  - "task_id"

post_install_suggestions:
  - "task_id"
```

### Field Reference

#### metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique profile identifier |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | Brief description |
| `version` | string | No | Profile version |

#### selection_prompt

How this profile appears in the initial stack selection.

```yaml
selection_prompt:
  letter: "A"
  text: "Full-Stack Web - JavaScript/TypeScript, React, Node.js, PostgreSQL"
```

#### required_tasks

Tasks always installed for this profile.

```yaml
required_tasks:
  - homebrew
```

#### question_flow

Ordered list of questions to ask the user.

Each question:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique question identifier |
| `question` | string | Question text to display |
| `options` | array | Available choices |

Each option:

| Field | Type | Description |
|-------|------|-------------|
| `letter` | string | A, B, C, D, or E |
| `text` | string | Option text with brief description |
| `tasks` | array | Task IDs to include if chosen |
| `action` | string | Special action (e.g., "explain") |
| `user_data_required` | array | Data to collect (e.g., ["git_name"]) |

**Example**:
```yaml
question_flow:
  - id: "editor"
    question: "Which editor do you prefer?"
    options:
      - letter: "A"
        text: "VS Code - Free, extensive extension ecosystem"
        tasks: ["vscode"]
      - letter: "B"
        text: "Cursor - AI-powered, built on VS Code"
        tasks: ["cursor"]
      - letter: "C"
        text: "Neovim - Terminal-based, highly customizable"
        tasks: ["neovim"]
      - letter: "D"
        text: "Not sure - Help me decide"
        action: "explain"
```

#### default_cli_tools

CLI tools included by default (user can remove from plan).

```yaml
default_cli_tools:
  - git
  - gh
  - jq
  - ripgrep
  - fzf
```

#### post_install_suggestions

Tasks to suggest after main installation completes.

```yaml
post_install_suggestions:
  - typescript-global
  - prettier-global
```

---

## Complete Example: Version Managers

```yaml
metadata:
  category: "version-managers"
  description: "Language version management tools"
  author: "agentic-provision"
  version: "1.0.0"
  created: "2026-02-02"

tasks:
  nvm:
    id: "nvm"
    name: "Node Version Manager (nvm)"
    description: "Manage multiple Node.js versions"
    category: "version-managers"
    tags: ["node", "javascript", "version-manager"]

    detection:
      check_command: "command -v nvm"
      version_command: "nvm --version"
      installed_indicator: "~/.nvm/nvm.sh"

    dependencies:
      required: []

    install:
      steps:
        - name: "Install nvm"
          command: 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash'
          description: "Download and run nvm installer"
          idempotent: false

    shell_integration:
      zsh: |
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
      bash: |
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    post_install:
      - task: "node-lts"
        condition: "user_choice"
        prompt: "Install Node.js LTS?"

    verification:
      command: "source ~/.nvm/nvm.sh && nvm --version"
      expected_pattern: "^\\d+\\.\\d+\\.\\d+$"

    conflicts_with: ["fnm", "volta", "asdf-nodejs"]

    notes: |
      nvm is the most widely-used Node version manager. It loads on shell
      startup which can add ~200ms to terminal launch. Consider fnm if
      you prefer faster shell startup.

    docs_url: "https://github.com/nvm-sh/nvm"

  fnm:
    id: "fnm"
    name: "Fast Node Manager (fnm)"
    description: "Fast, Rust-based Node.js version manager"
    category: "version-managers"
    tags: ["node", "javascript", "version-manager", "fast", "rust"]

    detection:
      check_command: "command -v fnm"
      version_command: "fnm --version"

    dependencies:
      required: ["homebrew"]

    install:
      steps:
        - name: "Install fnm via Homebrew"
          command: "brew install fnm"
          description: "Install fnm package manager"
          idempotent: true

    shell_integration:
      zsh: 'eval "$(fnm env --use-on-cd)"'
      bash: 'eval "$(fnm env --use-on-cd)"'

    post_install:
      - task: "node-lts"
        condition: "user_choice"
        prompt: "Install Node.js LTS?"

    verification:
      command: "fnm --version"
      expected_pattern: "^fnm \\d+\\.\\d+\\.\\d+$"

    conflicts_with: ["nvm", "volta", "asdf-nodejs"]

    notes: |
      fnm is a fast alternative to nvm, written in Rust. It has much
      faster shell startup time and supports automatic version switching
      via .nvmrc and .node-version files.

    docs_url: "https://github.com/Schniz/fnm"
```

---

## Complete Example: Profile

```yaml
metadata:
  id: "fullstack-web"
  name: "Full-Stack Web Development"
  description: "JavaScript/TypeScript, React, Node.js, PostgreSQL"
  version: "1.0.0"

selection_prompt:
  letter: "A"
  text: "Full-Stack Web - JavaScript/TypeScript, React, Node.js, PostgreSQL"

required_tasks:
  - homebrew

question_flow:
  - id: "js_runtime"
    question: "Which JavaScript runtime setup do you prefer?"
    options:
      - letter: "A"
        text: "Node.js via nvm - Version management, most widely used"
        tasks: ["nvm", "node-lts"]
      - letter: "B"
        text: "Node.js via fnm - Faster alternative to nvm"
        tasks: ["fnm", "node-lts"]
      - letter: "C"
        text: "Bun - Modern all-in-one runtime and package manager"
        tasks: ["bun"]
      - letter: "D"
        text: "Not sure - Help me decide"
        action: "explain"

  - id: "editor"
    question: "Which editor do you prefer?"
    options:
      - letter: "A"
        text: "VS Code - Free, extensive extension ecosystem"
        tasks: ["vscode"]
      - letter: "B"
        text: "Cursor - AI-powered, built on VS Code"
        tasks: ["cursor"]
      - letter: "C"
        text: "Neovim - Terminal-based, highly customizable"
        tasks: ["neovim"]
      - letter: "D"
        text: "JetBrains WebStorm - Full IDE experience"
        tasks: ["webstorm"]

  - id: "database"
    question: "Do you need a local database?"
    options:
      - letter: "A"
        text: "PostgreSQL - Reliable, feature-rich relational database"
        tasks: ["postgresql"]
      - letter: "B"
        text: "MySQL - Popular alternative to PostgreSQL"
        tasks: ["mysql"]
      - letter: "C"
        text: "MongoDB - Document database for flexible schemas"
        tasks: ["mongodb"]
      - letter: "D"
        text: "None - I use cloud databases or don't need one locally"
        tasks: []

  - id: "docker"
    question: "Do you need Docker for local development?"
    options:
      - letter: "A"
        text: "Yes - I run services in containers"
        tasks: ["docker-desktop"]
      - letter: "B"
        text: "No - I run everything directly on macOS"
        tasks: []
      - letter: "C"
        text: "Colima - Lightweight Docker alternative"
        tasks: ["colima"]
      - letter: "D"
        text: "Skip for now - I can add it later"
        tasks: []

  - id: "shell"
    question: "Do you want shell customization?"
    options:
      - letter: "A"
        text: "Starship - Fast, minimal, cross-shell prompt"
        tasks: ["starship"]
      - letter: "B"
        text: "Oh My Zsh - Popular framework with plugins"
        tasks: ["oh-my-zsh"]
      - letter: "C"
        text: "Powerlevel10k - Feature-rich zsh theme"
        tasks: ["powerlevel10k"]
      - letter: "D"
        text: "None - Keep the default shell as-is"
        tasks: []

  - id: "git"
    question: "Last question - do you need help setting up Git and GitHub?"
    options:
      - letter: "A"
        text: "Yes - Configure git and generate SSH keys"
        tasks: ["git-config", "ssh-keygen", "gh-cli"]
        user_data_required: ["git_name", "git_email"]
      - letter: "B"
        text: "Just git config - I'll handle SSH keys myself"
        tasks: ["git-config"]
        user_data_required: ["git_name", "git_email"]
      - letter: "C"
        text: "No - Already configured on this machine"
        tasks: []
      - letter: "D"
        text: "What's involved? - Explain first"
        action: "explain"

default_cli_tools:
  - git
  - gh
  - jq
  - ripgrep
  - fzf

post_install_suggestions:
  - typescript-global
  - prettier-global
  - eslint-global
```

---

## Agent Guidelines for Using Manifests

### Reading Manifests

1. Load manifests at session start
2. Use task definitions as reference (not strict execution rules)
3. Check `detection` before suggesting installation
4. Respect `conflicts_with` warnings
5. Follow `dependencies` order

### Executing Tasks

1. Show user the command from `install.steps`
2. Execute commands directly (not via manifest engine)
3. Record results in session state
4. Run `verification` after installation
5. Add `shell_integration` if applicable

### Creating Custom Tasks

When user requests something not in manifests:

1. Research the tool (using knowledge base + web if needed)
2. Generate task definition following this schema
3. Save to `~/.agentic-provision/tasks/custom/<tool>.yaml`
4. Record in session that custom task was created
5. Use the new definition for installation

### Manifest Validation

Before using a manifest, verify:

- [ ] All required fields present
- [ ] `id` matches the key
- [ ] `dependencies` reference existing tasks
- [ ] `conflicts_with` references existing tasks
- [ ] Commands are valid shell syntax
