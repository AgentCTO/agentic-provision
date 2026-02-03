#!/usr/bin/env python3
"""
Agentic Provision - Claude Agent SDK Integration

Uses the official Claude Agent SDK for tool execution while maintaining
our custom state persistence layer for session management and resume capability.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add lib to path
LIB_DIR = Path(__file__).parent
sys.path.insert(0, str(LIB_DIR))

from state_manager import SessionState

# Try to import the Claude Agent SDK
try:
    from claude_agent_sdk import (
        query,
        ClaudeAgentOptions,
        AssistantMessage,
        ResultMessage,
        ToolUseMessage,
        ToolResultMessage,
        tool,
        create_sdk_mcp_server,
    )
except ImportError:
    print("Error: claude-agent-sdk not installed.")
    print("Run: pip install claude-agent-sdk")
    sys.exit(1)

# Try to import yaml
try:
    import yaml
except ImportError:
    yaml = None


# =============================================================================
# Configuration
# =============================================================================

PROVISION_DIR = Path(os.environ.get("AGENTIC_PROVISION_DIR", Path.home() / ".agentic-provision"))
KNOWLEDGE_DIR = PROVISION_DIR / "knowledge"
TASKS_DIR = PROVISION_DIR / "tasks"
SESSIONS_DIR = PROVISION_DIR / "sessions"

# Global state instance
state: Optional[SessionState] = None


# =============================================================================
# Custom MCP Tools for State Management
# =============================================================================

@tool("state_create_session", "Create a new provisioning session", {
    "profile": {"type": "string", "description": "Profile name (e.g., 'fullstack-web')"}
})
async def create_session(args: Dict[str, Any]):
    """Create a new session and return the session ID."""
    global state
    state = SessionState(str(SESSIONS_DIR))
    session_id = state.create_session(args.get("profile"))
    return {
        "content": [{"type": "text", "text": json.dumps({
            "session_id": session_id,
            "path": str(state.session_file)
        })}]
    }


@tool("state_load_session", "Load an existing session to resume", {
    "path": {"type": "string", "description": "Path to session JSON file"}
})
async def load_session(args: Dict[str, Any]):
    """Load an existing session."""
    global state
    state = SessionState(str(SESSIONS_DIR))
    state_data = state.load_session(args["path"])
    return {
        "content": [{"type": "text", "text": json.dumps({
            "loaded": True,
            "session_id": state_data["meta"]["id"],
            "status": state_data["meta"]["status"],
            "phase": state_data["phase"]["current"]
        })}]
    }


@tool("state_record_choice", "Record user's answer to a question", {
    "question_id": {"type": "string", "description": "Question identifier"},
    "answer": {"type": "string", "description": "Letter chosen (A, B, etc.)"},
    "value": {"type": "string", "description": "Actual value selected"}
})
async def record_choice(args: Dict[str, Any]):
    """Record a user choice."""
    if state:
        state.record_choice(args["question_id"], args["answer"], args["value"])
        return {"content": [{"type": "text", "text": "Choice recorded"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_record_user_data", "Record user-provided data", {
    "key": {"type": "string", "description": "Data key (git_name, git_email, etc.)"},
    "value": {"type": "string", "description": "Value provided by user"}
})
async def record_user_data(args: Dict[str, Any]):
    """Record user-provided data."""
    if state:
        state.record_user_data(args["key"], args["value"])
        return {"content": [{"type": "text", "text": f"Recorded {args['key']}"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_set_phase", "Transition to a new phase", {
    "phase": {"type": "string", "description": "Phase: init, requirements, plan, execute, complete"}
})
async def set_phase(args: Dict[str, Any]):
    """Set the current phase."""
    if state:
        state.set_phase(args["phase"])
        return {"content": [{"type": "text", "text": f"Phase: {args['phase']}"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_set_plan", "Set the installation plan", {
    "tasks": {"type": "array", "items": {"type": "string"}, "description": "List of task IDs"}
})
async def set_plan(args: Dict[str, Any]):
    """Set the installation plan."""
    if state:
        state.set_plan(args["tasks"])
        return {"content": [{"type": "text", "text": json.dumps({
            "plan_set": True,
            "tasks": args["tasks"]
        })}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_start_task", "Mark a task as started", {
    "task_id": {"type": "string", "description": "Task ID being started"}
})
async def start_task(args: Dict[str, Any]):
    """Mark a task as started."""
    if state:
        state.start_task(args["task_id"])
        return {"content": [{"type": "text", "text": f"Started: {args['task_id']}"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_complete_task", "Mark a task as completed", {
    "task_id": {"type": "string", "description": "Task ID that completed"}
})
async def complete_task(args: Dict[str, Any]):
    """Mark a task as completed."""
    if state:
        state.complete_task(args["task_id"])
        return {"content": [{"type": "text", "text": f"Completed: {args['task_id']}"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_fail_task", "Mark a task as failed", {
    "task_id": {"type": "string", "description": "Task ID that failed"},
    "error": {"type": "string", "description": "Error message"}
})
async def fail_task(args: Dict[str, Any]):
    """Mark a task as failed."""
    if state:
        state.fail_task(args["task_id"], args["error"])
        return {"content": [{"type": "text", "text": f"Failed: {args['task_id']}"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_skip_task", "Mark a task as skipped", {
    "task_id": {"type": "string", "description": "Task ID being skipped"}
})
async def skip_task(args: Dict[str, Any]):
    """Mark a task as skipped."""
    if state:
        state.skip_task(args["task_id"])
        return {"content": [{"type": "text", "text": f"Skipped: {args['task_id']}"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_complete_session", "Mark the session as complete", {})
async def complete_session(args: Dict[str, Any]):
    """Mark session as completed."""
    if state:
        state.complete_session()
        return {"content": [{"type": "text", "text": "Session completed"}]}
    return {"content": [{"type": "text", "text": "Error: No active session"}]}


@tool("state_get_current", "Get the current session state", {})
async def get_current(args: Dict[str, Any]):
    """Get current session state."""
    if state:
        return {"content": [{"type": "text", "text": json.dumps(state.state, indent=2)}]}
    return {"content": [{"type": "text", "text": json.dumps({"error": "No active session"})}]}


@tool("parse_yaml", "Parse a YAML file and return as JSON", {
    "path": {"type": "string", "description": "Path to YAML file"}
})
async def parse_yaml(args: Dict[str, Any]):
    """Parse YAML file."""
    if yaml is None:
        return {"content": [{"type": "text", "text": json.dumps({"error": "PyYAML not installed"})}]}

    path = Path(args["path"])
    try:
        if not path.exists():
            return {"content": [{"type": "text", "text": json.dumps({"error": f"File not found: {path}"})}]}

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        return {"content": [{"type": "text", "text": json.dumps({"content": data})}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": json.dumps({"error": str(e)})}]}


@tool("list_sessions", "List existing provisioning sessions", {
    "status": {"type": "string", "description": "Filter by status: active, completed, failed, or all"}
})
async def list_sessions(args: Dict[str, Any]):
    """List existing sessions."""
    status = args.get("status", "all")
    sessions = []

    dirs_to_check = []
    if status in ["active", "all"]:
        dirs_to_check.append(("active", SESSIONS_DIR / "active"))
    if status in ["completed", "all"]:
        dirs_to_check.append(("completed", SESSIONS_DIR / "completed"))
    if status in ["failed", "all"]:
        dirs_to_check.append(("failed", SESSIONS_DIR / "failed"))

    for status_name, dir_path in dirs_to_check:
        if dir_path.exists():
            for f in dir_path.glob("*.json"):
                try:
                    with open(f) as fp:
                        data = json.load(fp)
                    sessions.append({
                        "path": str(f),
                        "id": data.get("meta", {}).get("id"),
                        "status": status_name,
                        "profile": data.get("profile"),
                        "created": data.get("meta", {}).get("created"),
                        "updated": data.get("meta", {}).get("updated")
                    })
                except:
                    pass

    # Sort by updated time, most recent first
    sessions.sort(key=lambda x: x.get("updated", ""), reverse=True)

    return {"content": [{"type": "text", "text": json.dumps({"sessions": sessions, "count": len(sessions)})}]}


# =============================================================================
# Create MCP Server with all state tools
# =============================================================================

state_mcp_server = create_sdk_mcp_server(
    name="provisioning-state",
    version="1.0.0",
    tools=[
        create_session,
        load_session,
        record_choice,
        record_user_data,
        set_phase,
        set_plan,
        start_task,
        complete_task,
        fail_task,
        skip_task,
        complete_session,
        get_current,
        parse_yaml,
        list_sessions,
    ]
)


# =============================================================================
# System Prompt Loading
# =============================================================================

def load_system_prompt() -> str:
    """Load system prompt with runtime context."""
    prompt_path = KNOWLEDGE_DIR / "system-prompt.md"
    if prompt_path.exists():
        base_prompt = prompt_path.read_text()
    else:
        base_prompt = "You are a macOS provisioning assistant."

    # Add runtime context
    runtime_context = f"""

---

## Runtime Context

You are running via the Claude Agent SDK with full tool access.

**Paths:**
- Knowledge Directory: {KNOWLEDGE_DIR}
- Tasks Directory: {TASKS_DIR}
- Sessions Directory: {SESSIONS_DIR}

**Available Tools:**
- Built-in: Read, Write, Bash, Edit, Glob, Grep
- State Management: state_create_session, state_load_session, state_record_choice,
  state_record_user_data, state_set_phase, state_set_plan, state_start_task,
  state_complete_task, state_fail_task, state_skip_task, state_complete_session,
  state_get_current
- Utilities: parse_yaml, list_sessions

**Session Detection:**
"""

    # Check for existing sessions
    active_sessions = list((SESSIONS_DIR / "active").glob("*.json")) if (SESSIONS_DIR / "active").exists() else []
    failed_sessions = list((SESSIONS_DIR / "failed").glob("*.json")) if (SESSIONS_DIR / "failed").exists() else []
    completed_sessions = list((SESSIONS_DIR / "completed").glob("*.json")) if (SESSIONS_DIR / "completed").exists() else []

    if active_sessions:
        latest = max(active_sessions, key=lambda p: p.stat().st_mtime)
        runtime_context += f"\n- **Active Session**: {latest}"
    if failed_sessions:
        latest = max(failed_sessions, key=lambda p: p.stat().st_mtime)
        runtime_context += f"\n- **Failed Session**: {latest}"
    if completed_sessions:
        latest = max(completed_sessions, key=lambda p: p.stat().st_mtime)
        runtime_context += f"\n- **Completed Session**: {latest}"

    if not (active_sessions or failed_sessions or completed_sessions):
        runtime_context += "\nNo existing sessions found. Start fresh with Phase 1."

    return base_prompt + runtime_context


# =============================================================================
# Main Entry Point
# =============================================================================

async def run_provisioner(auto_approve: bool = False):
    """Main provisioner loop using Claude Agent SDK."""

    print("\n" + "═" * 60)
    print("  🤖 Agentic Provision")
    print("  AI-assisted Mac development setup")
    print("═" * 60 + "\n")

    # Configure permission mode based on auto_approve
    if auto_approve:
        permission_mode = "bypassPermissions"
    else:
        permission_mode = "acceptEdits"  # Auto-approve file edits, prompt for Bash

    options = ClaudeAgentOptions(
        # Built-in Claude Code tools
        allowed_tools=["Read", "Write", "Bash", "Edit", "Glob", "Grep"],

        # Our custom state management MCP server
        mcp_servers={"state": state_mcp_server},

        # Permission handling
        permission_mode=permission_mode,

        # Our provisioning system prompt
        system_prompt=load_system_prompt(),

        # Working directory
        cwd=str(Path.home()),
    )

    try:
        # Stream messages as Claude works
        async for message in query(
            prompt="Begin",  # System prompt tells agent to speak first
            options=options
        ):
            if isinstance(message, AssistantMessage):
                # Print Claude's text output
                for block in message.content:
                    if hasattr(block, "text"):
                        print(block.text, end="", flush=True)
                    elif hasattr(block, "name"):
                        # Tool being called - show indicator
                        print(f"\n[Using: {block.name}]", flush=True)

            elif isinstance(message, ToolResultMessage):
                # Tool result - could log to state here
                pass

            elif isinstance(message, ResultMessage):
                # Session ended
                print(f"\n\n[Session ended: {message.subtype}]")
                break

    except KeyboardInterrupt:
        print("\n\nInterrupted. Saving state...")
        if state and state.state.get("meta", {}).get("status") == "active":
            state.state["meta"]["status"] = "interrupted"
            state._save()
        print("State saved. Goodbye!")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Agentic Provision - AI-assisted Mac setup")
    parser.add_argument("-y", "--auto-approve", action="store_true",
                        help="Skip all confirmation prompts")
    args = parser.parse_args()

    # Check for API key (Claude Code handles this, but good to verify)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        # Claude Code may use its own auth, so just warn
        print("Note: ANTHROPIC_API_KEY not set. Using Claude Code authentication.")

    # Run the async provisioner
    asyncio.run(run_provisioner(auto_approve=args.auto_approve))


if __name__ == "__main__":
    main()
