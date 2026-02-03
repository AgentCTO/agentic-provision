#!/usr/bin/env python3
"""
Agentic Provision - Deterministic State Manager

This module provides robust, non-LLM-dependent state management for provisioning sessions.
State is automatically persisted after every command execution via hooks.

The LLM is only responsible for semantic state (user choices, phase transitions).
Mechanical state (command execution, success/failure) is handled deterministically.
"""

import json
import os
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import random
import string


class SessionState:
    """Manages session state with atomic writes and crash recovery."""

    def __init__(self, sessions_dir: str):
        self.sessions_dir = Path(sessions_dir)
        self.active_dir = self.sessions_dir / "active"
        self.completed_dir = self.sessions_dir / "completed"
        self.failed_dir = self.sessions_dir / "failed"

        self.session_file: Optional[Path] = None
        self.state: Dict[str, Any] = {}

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

    def _generate_session_id(self) -> str:
        """Generate a unique session ID: prov-YYYYMMDD-HHMMSS-XXXX"""
        now = datetime.now()
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return f"prov-{now.strftime('%Y%m%d-%H%M%S')}-{random_suffix}"

    def create_session(self, profile: Optional[str] = None) -> str:
        """Create a new session and return the session ID."""
        session_id = self._generate_session_id()

        self.state = {
            "meta": {
                "id": session_id,
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "status": "active",
                "version": "1.0"
            },
            "phase": {
                "current": "init",
                "history": []
            },
            "profile": profile,
            "choices": {},
            "user_data": {},
            "tasks": {},
            "plan": [],
            "execution": {
                "commands": [],
                "current_task": None
            },
            "resume_point": None,
            "expansion_history": []
        }

        self.session_file = self.active_dir / f"{session_id}.json"
        self._save()

        return session_id

    def load_session(self, session_path: str) -> Dict[str, Any]:
        """Load an existing session from file."""
        self.session_file = Path(session_path)

        if not self.session_file.exists():
            raise FileNotFoundError(f"Session file not found: {session_path}")

        with open(self.session_file, 'r') as f:
            self.state = json.load(f)

        return self.state

    def _save(self) -> None:
        """Atomically save state to file."""
        if not self.session_file:
            return

        self.state["meta"]["updated"] = datetime.now().isoformat()

        # Write to temp file first, then rename (atomic on POSIX)
        tmp_file = self.session_file.with_suffix('.tmp')
        with open(tmp_file, 'w') as f:
            json.dump(self.state, f, indent=2)

        tmp_file.rename(self.session_file)

    def update(self, updates: Dict[str, Any]) -> None:
        """Update state with new values and save."""
        self._deep_update(self.state, updates)
        self._save()

    def _deep_update(self, base: dict, updates: dict) -> None:
        """Recursively update nested dictionaries."""
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    # -------------------------------------------------------------------------
    # Phase Management
    # -------------------------------------------------------------------------

    def set_phase(self, phase: str) -> None:
        """Transition to a new phase."""
        current = self.state["phase"]["current"]
        if current != phase:
            self.state["phase"]["history"].append({
                "phase": current,
                "ended": datetime.now().isoformat()
            })
            self.state["phase"]["current"] = phase
            self._save()

    # -------------------------------------------------------------------------
    # Choice Recording (Semantic - called by LLM)
    # -------------------------------------------------------------------------

    def record_choice(self, question_id: str, answer: str, value: Any) -> None:
        """Record a user choice."""
        self.state["choices"][question_id] = {
            "answer": answer,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save()

    def record_user_data(self, key: str, value: str) -> None:
        """Record user-provided data (name, email, etc.)."""
        self.state["user_data"][key] = value
        self._save()

    # -------------------------------------------------------------------------
    # Task Management (Mechanical - called by hooks)
    # -------------------------------------------------------------------------

    def set_plan(self, tasks: list) -> None:
        """Set the installation plan."""
        self.state["plan"] = tasks
        for task_id in tasks:
            if task_id not in self.state["tasks"]:
                self.state["tasks"][task_id] = {"status": "pending"}
        self._save()

    def start_task(self, task_id: str) -> None:
        """Mark a task as started."""
        self.state["execution"]["current_task"] = task_id
        self.state["tasks"][task_id] = {
            "status": "in_progress",
            "started": datetime.now().isoformat()
        }
        self.state["resume_point"] = {
            "task_id": task_id,
            "action": "retry"
        }
        self._save()

    def complete_task(self, task_id: str) -> None:
        """Mark a task as completed."""
        self.state["tasks"][task_id]["status"] = "completed"
        self.state["tasks"][task_id]["completed"] = datetime.now().isoformat()
        self.state["execution"]["current_task"] = None
        self._save()

    def fail_task(self, task_id: str, error: str) -> None:
        """Mark a task as failed."""
        self.state["tasks"][task_id]["status"] = "failed"
        self.state["tasks"][task_id]["error"] = error[:500]  # Truncate long errors
        self.state["tasks"][task_id]["failed_at"] = datetime.now().isoformat()
        self.state["resume_point"] = {
            "task_id": task_id,
            "action": "retry_or_skip",
            "error": error[:200]
        }
        self._save()

    def skip_task(self, task_id: str) -> None:
        """Mark a task as skipped."""
        self.state["tasks"][task_id] = {
            "status": "skipped",
            "skipped_at": datetime.now().isoformat()
        }
        self._save()

    # -------------------------------------------------------------------------
    # Command Logging (Mechanical - called by hooks)
    # -------------------------------------------------------------------------

    def log_command_start(self, command: str, language: str) -> int:
        """Log the start of a command execution. Returns command index."""
        cmd_entry = {
            "command": command[:1000],  # Truncate very long commands
            "language": language,
            "started": datetime.now().isoformat(),
            "status": "running"
        }
        self.state["execution"]["commands"].append(cmd_entry)
        self._save()
        return len(self.state["execution"]["commands"]) - 1

    def log_command_end(self, index: int, success: bool, output: str = "", error: str = "") -> None:
        """Log the completion of a command execution."""
        if index < len(self.state["execution"]["commands"]):
            cmd = self.state["execution"]["commands"][index]
            cmd["ended"] = datetime.now().isoformat()
            cmd["status"] = "success" if success else "failed"
            if output:
                cmd["output"] = output[:500]  # Truncate long output
            if error:
                cmd["error"] = error[:500]
            self._save()

    # -------------------------------------------------------------------------
    # Session Lifecycle
    # -------------------------------------------------------------------------

    def complete_session(self) -> None:
        """Mark session as completed and move to completed directory."""
        self.state["meta"]["status"] = "completed"
        self.state["meta"]["completed"] = datetime.now().isoformat()
        self._save()

        # Move to completed directory
        if self.session_file and self.session_file.parent == self.active_dir:
            new_path = self.completed_dir / self.session_file.name
            self.session_file.rename(new_path)
            self.session_file = new_path

    def fail_session(self, reason: str = "") -> None:
        """Mark session as failed and move to failed directory."""
        self.state["meta"]["status"] = "failed"
        self.state["meta"]["failed_at"] = datetime.now().isoformat()
        if reason:
            self.state["meta"]["failure_reason"] = reason[:500]
        self._save()

        # Move to failed directory
        if self.session_file and self.session_file.parent == self.active_dir:
            new_path = self.failed_dir / self.session_file.name
            self.session_file.rename(new_path)
            self.session_file = new_path

    def _handle_shutdown(self, signum, frame) -> None:
        """Handle graceful shutdown on SIGTERM/SIGINT."""
        if self.state.get("meta", {}).get("status") == "active":
            self.state["meta"]["status"] = "interrupted"
            self.state["meta"]["interrupted_at"] = datetime.now().isoformat()
            self._save()
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Query Methods
    # -------------------------------------------------------------------------

    def get_completed_tasks(self) -> list:
        """Get list of completed task IDs."""
        return [
            task_id for task_id, info in self.state.get("tasks", {}).items()
            if info.get("status") == "completed"
        ]

    def get_pending_tasks(self) -> list:
        """Get list of pending task IDs."""
        return [
            task_id for task_id, info in self.state.get("tasks", {}).items()
            if info.get("status") == "pending"
        ]

    def get_failed_task(self) -> Optional[Dict[str, Any]]:
        """Get the failed task info, if any."""
        for task_id, info in self.state.get("tasks", {}).items():
            if info.get("status") == "failed":
                return {"task_id": task_id, **info}
        return None


# Global state instance (initialized by launcher)
_state: Optional[SessionState] = None


def init_state_manager(sessions_dir: str) -> SessionState:
    """Initialize the global state manager."""
    global _state
    _state = SessionState(sessions_dir)
    return _state


def get_state_manager() -> Optional[SessionState]:
    """Get the global state manager instance."""
    return _state


# -------------------------------------------------------------------------
# Open Interpreter Hooks Integration
# -------------------------------------------------------------------------
# These functions are called by Open Interpreter if configured with hooks

def before_command(interpreter, command: str, language: str) -> None:
    """Hook called before command execution."""
    if _state:
        _state.log_command_start(command, language)


def after_command(interpreter, command: str, language: str, output: str, error: str) -> None:
    """Hook called after command execution."""
    if _state:
        # Find the most recent command entry
        commands = _state.state.get("execution", {}).get("commands", [])
        if commands:
            index = len(commands) - 1
            success = error is None or error == ""
            _state.log_command_end(index, success, output or "", error or "")

            # If this was a task command and it failed, mark task as failed
            current_task = _state.state.get("execution", {}).get("current_task")
            if current_task and not success:
                _state.fail_task(current_task, error or "Command failed")


if __name__ == "__main__":
    # Simple test
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_dir = Path(tmpdir)
        (sessions_dir / "active").mkdir(parents=True)
        (sessions_dir / "completed").mkdir(parents=True)
        (sessions_dir / "failed").mkdir(parents=True)

        state = init_state_manager(str(sessions_dir))
        session_id = state.create_session("fullstack-web")
        print(f"Created session: {session_id}")

        state.set_phase("requirements")
        state.record_choice("runtime", "A", "nvm")
        state.set_plan(["homebrew", "nvm", "node-lts"])

        state.start_task("homebrew")
        state.log_command_start("brew --version", "bash")
        state.log_command_end(0, True, "Homebrew 4.2.0")
        state.complete_task("homebrew")

        print(f"State: {json.dumps(state.state, indent=2)}")
        print("Test passed!")
