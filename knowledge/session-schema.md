# Session State Schema

This document defines the JSON schema for provisioning session state files.

## Overview

Session state files track the complete state of a provisioning session, enabling:
- **Resume**: Continue from where a failed/interrupted session stopped
- **Audit**: Review what was installed and when
- **Expansion**: Add new tools to an existing setup

## File Locations

```
~/.agentic-provision/sessions/
├── active/           # Sessions currently in progress
│   └── <session-id>.json
├── completed/        # Successfully finished sessions
│   └── <session-id>.json
└── failed/           # Sessions that stopped due to error
    └── <session-id>.json
```

## Session ID Format

```
prov-YYYYMMDD-HHMMSS-XXXX
```

- `prov` - Prefix for provisioning sessions
- `YYYYMMDD` - Date (e.g., 20260202)
- `HHMMSS` - Time in 24-hour format (e.g., 143052)
- `XXXX` - Random 4-character hex suffix for uniqueness

Example: `prov-20260202-143052-a7b3`

---

## Complete Schema

```json
{
  "meta": {
    "id": "string",
    "created_at": "ISO-8601 timestamp",
    "updated_at": "ISO-8601 timestamp",
    "status": "in_progress | completed | failed | paused",
    "version": "1.0.0",
    "machine": {
      "hostname": "string",
      "os_version": "string",
      "arch": "arm64 | x86_64",
      "chip": "string (e.g., Apple M3 Pro)"
    }
  },

  "phase": {
    "current": "session_check | stack_selection | gather_requirements | present_plan | execute | completion",
    "history": [
      {
        "phase": "string",
        "completed_at": "ISO-8601 timestamp"
      }
    ]
  },

  "profile": {
    "selected": "string (profile id)",
    "manifest_path": "string (path to profile YAML)",
    "base_tasks": ["array", "of", "task", "ids"]
  },

  "choices": {
    "<question_id>": {
      "question": "string (the question asked)",
      "answer": "string (A, B, C, D, or E)",
      "value": "string (semantic value of choice)",
      "timestamp": "ISO-8601 timestamp"
    }
  },

  "user_data": {
    "<key>": "value (user-provided data like git_name, git_email)"
  },

  "tasks": {
    "<task_id>": {
      "task_id": "string",
      "status": "pending | in_progress | completed | failed | skipped",
      "skipped": "boolean",
      "skipped_reason": "string (optional)",
      "started_at": "ISO-8601 timestamp (optional)",
      "completed_at": "ISO-8601 timestamp (optional)",
      "failed_at": "ISO-8601 timestamp (optional)",
      "commands": [
        {
          "command": "string (the command executed)",
          "description": "string (what this command does)",
          "status": "success | failed | skipped",
          "exit_code": "number (optional)",
          "error": "string (optional, error message if failed)",
          "output_summary": "string (optional, brief output summary)",
          "user_choice": "string (A, B, C, D - user's response)",
          "retry_count": "number (default 0)",
          "executed_at": "ISO-8601 timestamp"
        }
      ],
      "result": {
        "<key>": "value (task-specific results like version numbers)"
      },
      "failure_context": {
        "error_type": "string (categorized error type)",
        "suggested_resolution": "string"
      }
    }
  },

  "plan": {
    "approved_at": "ISO-8601 timestamp",
    "execution_mode": "all_at_once | review_each_step",
    "categories": [
      {
        "name": "string (category name)",
        "items": ["array", "of", "item", "descriptions"]
      }
    ]
  },

  "resume_point": {
    "task_id": "string (task to resume from)",
    "command_index": "number (which command in the task)",
    "action": "retry | skip | choose",
    "context": "string (human-readable context)"
  },

  "expansion_history": [
    {
      "session_id": "string (previous session that was expanded)",
      "expanded_at": "ISO-8601 timestamp",
      "tasks_added": ["array", "of", "task", "ids"]
    }
  ]
}
```

---

## Field Descriptions

### meta

Session metadata and machine information.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique session identifier |
| `created_at` | ISO-8601 | When session was created |
| `updated_at` | ISO-8601 | Last modification time |
| `status` | enum | Current session status |
| `version` | string | Schema version for compatibility |
| `machine` | object | Machine identification |

**Status Values**:
- `in_progress` - Session is active
- `completed` - All tasks finished successfully
- `failed` - Session stopped due to unrecoverable error
- `paused` - User chose to pause and continue later

### phase

Tracks progression through the provisioning workflow.

| Field | Type | Description |
|-------|------|-------------|
| `current` | enum | Current phase |
| `history` | array | Completed phases with timestamps |

**Phase Values**:
1. `session_check` - Checking for existing sessions
2. `stack_selection` - User selecting development stack
3. `gather_requirements` - Collecting preferences via questions
4. `present_plan` - Showing installation plan for approval
5. `execute` - Installing tools and configurations
6. `completion` - Summarizing and offering next steps

### profile

Selected development profile information.

| Field | Type | Description |
|-------|------|-------------|
| `selected` | string | Profile ID (e.g., "fullstack-web") |
| `manifest_path` | string | Path to profile YAML file |
| `base_tasks` | array | Task IDs derived from profile |

### choices

All user responses during requirements gathering.

Each choice is keyed by `question_id` and contains:

| Field | Type | Description |
|-------|------|-------------|
| `question` | string | The question text shown to user |
| `answer` | string | Letter response (A-E) |
| `value` | string | Semantic meaning of the choice |
| `timestamp` | ISO-8601 | When choice was made |

### user_data

User-provided information collected during the session.

Common keys:
- `git_name` - User's name for git config
- `git_email` - User's email for git config
- `github_username` - GitHub username

### tasks

Status and execution history for each task.

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Unique task identifier |
| `status` | enum | Current task status |
| `skipped` | boolean | Whether task was skipped |
| `skipped_reason` | string | Why task was skipped |
| `started_at` | ISO-8601 | When execution started |
| `completed_at` | ISO-8601 | When execution completed |
| `failed_at` | ISO-8601 | When execution failed |
| `commands` | array | Individual commands executed |
| `result` | object | Task-specific results |
| `failure_context` | object | Error details if failed |

**Task Status Values**:
- `pending` - Not yet started
- `in_progress` - Currently executing
- `completed` - Successfully finished
- `failed` - Execution failed
- `skipped` - User chose to skip

### plan

The approved installation plan.

| Field | Type | Description |
|-------|------|-------------|
| `approved_at` | ISO-8601 | When user approved the plan |
| `execution_mode` | enum | How user wants to proceed |
| `categories` | array | Grouped items for display |

**Execution Modes**:
- `all_at_once` - Run everything with minimal prompts
- `review_each_step` - Confirm each command before running

### resume_point

Where to continue when resuming a session.

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Task to resume from |
| `command_index` | number | Which command (0-indexed) |
| `action` | enum | What action to offer |
| `context` | string | Human-readable explanation |

**Action Values**:
- `retry` - Retry the failed command
- `skip` - Skip and continue to next
- `choose` - Let user decide

### expansion_history

Record of previous sessions that were expanded.

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | ID of session being expanded |
| `expanded_at` | ISO-8601 | When expansion occurred |
| `tasks_added` | array | New tasks added in this expansion |

---

## Example: Fresh Session Start

```json
{
  "meta": {
    "id": "prov-20260202-143052-a7b3",
    "created_at": "2026-02-02T14:30:52Z",
    "updated_at": "2026-02-02T14:30:52Z",
    "status": "in_progress",
    "version": "1.0.0",
    "machine": {
      "hostname": "alexs-macbook",
      "os_version": "15.2",
      "arch": "arm64",
      "chip": "Apple M3 Pro"
    }
  },
  "phase": {
    "current": "stack_selection",
    "history": []
  },
  "profile": {},
  "choices": {},
  "user_data": {},
  "tasks": {},
  "plan": {},
  "resume_point": null,
  "expansion_history": []
}
```

## Example: Mid-Session (Execution Phase)

```json
{
  "meta": {
    "id": "prov-20260202-143052-a7b3",
    "created_at": "2026-02-02T14:30:52Z",
    "updated_at": "2026-02-02T14:45:23Z",
    "status": "in_progress",
    "version": "1.0.0",
    "machine": {
      "hostname": "alexs-macbook",
      "os_version": "15.2",
      "arch": "arm64",
      "chip": "Apple M3 Pro"
    }
  },
  "phase": {
    "current": "execute",
    "history": [
      {"phase": "stack_selection", "completed_at": "2026-02-02T14:31:15Z"},
      {"phase": "gather_requirements", "completed_at": "2026-02-02T14:38:42Z"},
      {"phase": "present_plan", "completed_at": "2026-02-02T14:39:10Z"}
    ]
  },
  "profile": {
    "selected": "fullstack-web",
    "manifest_path": "~/.agentic-provision/tasks/profiles/fullstack-web.yaml",
    "base_tasks": ["homebrew", "nvm", "node-lts", "cursor", "postgresql", "docker", "starship", "git-config"]
  },
  "choices": {
    "stack_type": {
      "question": "What type of development will you be doing?",
      "answer": "A",
      "value": "fullstack-web",
      "timestamp": "2026-02-02T14:31:15Z"
    },
    "js_runtime": {
      "question": "Which JavaScript runtime setup do you prefer?",
      "answer": "A",
      "value": "nvm",
      "timestamp": "2026-02-02T14:32:01Z"
    },
    "editor": {
      "question": "Which editor do you prefer?",
      "answer": "B",
      "value": "cursor",
      "timestamp": "2026-02-02T14:33:18Z"
    }
  },
  "user_data": {
    "git_name": "Alex Chen",
    "git_email": "alex@example.com"
  },
  "tasks": {
    "homebrew": {
      "task_id": "homebrew",
      "status": "completed",
      "skipped": false,
      "started_at": "2026-02-02T14:40:01Z",
      "completed_at": "2026-02-02T14:40:02Z",
      "commands": [
        {
          "command": "command -v brew",
          "description": "Check if Homebrew is installed",
          "status": "success",
          "exit_code": 0,
          "output_summary": "Already installed at /opt/homebrew/bin/brew",
          "user_choice": "A",
          "executed_at": "2026-02-02T14:40:01Z"
        }
      ],
      "result": {
        "version": "4.2.0",
        "path": "/opt/homebrew/bin/brew"
      }
    },
    "nvm": {
      "task_id": "nvm",
      "status": "completed",
      "skipped": false,
      "started_at": "2026-02-02T14:40:15Z",
      "completed_at": "2026-02-02T14:40:45Z",
      "commands": [
        {
          "command": "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash",
          "description": "Install nvm",
          "status": "success",
          "exit_code": 0,
          "user_choice": "A",
          "executed_at": "2026-02-02T14:40:20Z"
        }
      ]
    },
    "cursor": {
      "task_id": "cursor",
      "status": "failed",
      "skipped": false,
      "started_at": "2026-02-02T14:43:00Z",
      "failed_at": "2026-02-02T14:43:15Z",
      "commands": [
        {
          "command": "brew install --cask cursor",
          "description": "Install Cursor editor",
          "status": "failed",
          "exit_code": 1,
          "error": "Error: Cask 'cursor' requires a password to be set.",
          "user_choice": "A",
          "retry_count": 0,
          "executed_at": "2026-02-02T14:43:05Z"
        }
      ],
      "failure_context": {
        "error_type": "permission_required",
        "suggested_resolution": "Run with password prompt or skip"
      }
    },
    "postgresql": {
      "task_id": "postgresql",
      "status": "pending",
      "skipped": false
    }
  },
  "plan": {
    "approved_at": "2026-02-02T14:39:10Z",
    "execution_mode": "review_each_step",
    "categories": [
      {"name": "Package Manager", "items": ["Homebrew"]},
      {"name": "Languages & Runtime", "items": ["Node.js 20 (LTS) via nvm"]},
      {"name": "Editor", "items": ["Cursor"]},
      {"name": "Database", "items": ["PostgreSQL 16"]}
    ]
  },
  "resume_point": {
    "task_id": "cursor",
    "command_index": 0,
    "action": "choose",
    "context": "Cursor installation failed with permission error"
  },
  "expansion_history": []
}
```

---

## State Transitions

### Session Status Transitions

```
                    ┌──────────────┐
                    │  in_progress │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ completed│    │  failed  │    │  paused  │
    └──────────┘    └────┬─────┘    └────┬─────┘
                         │               │
                         └───────┬───────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │  in_progress │ (on resume)
                          └──────────────┘
```

### Task Status Transitions

```
    ┌─────────┐
    │ pending │
    └────┬────┘
         │
         ▼
    ┌─────────────┐
    │ in_progress │
    └──────┬──────┘
           │
    ┌──────┼──────┬──────────┐
    │      │      │          │
    ▼      ▼      ▼          ▼
┌─────┐ ┌─────┐ ┌──────┐ ┌───────┐
│done │ │fail │ │skip  │ │pending│ (on retry)
└─────┘ └──┬──┘ └──────┘ └───────┘
           │
           ▼
      ┌─────────────┐
      │ in_progress │ (on retry)
      └─────────────┘
```

---

## Persistence Rules

1. **Save immediately** after every state change
2. **Update `updated_at`** on every save
3. **Never lose data** - write to temp file first, then rename
4. **Pretty-print JSON** with 2-space indentation for readability
5. **Move between directories** based on status changes:
   - `in_progress` / `paused` → `active/`
   - `completed` → `completed/`
   - `failed` → `failed/`
