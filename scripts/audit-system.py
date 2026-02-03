#!/usr/bin/env python3
"""
System Audit Tool for Agentic Provision

Scans the system for installed tools and generates a comprehensive report.
Used by the agent to understand current state before making recommendations.

Usage:
    ./audit-system.py                    # Full audit, human-readable
    ./audit-system.py --json             # Machine-readable JSON output
    ./audit-system.py --category editors # Audit specific category
    ./audit-system.py --diff session.json # Compare against session state
    ./audit-system.py --quick            # Fast audit (skip slow checks)
"""

import argparse
import json
import subprocess
import sys
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
import concurrent.futures

# Find project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

@dataclass
class ToolStatus:
    task_id: str
    name: str
    category: str
    installed: bool
    version: Optional[str] = None
    install_path: Optional[str] = None
    detection_method: str = ""
    error: Optional[str] = None

@dataclass
class SystemInfo:
    hostname: str = ""
    macos_version: str = ""
    architecture: str = ""
    shell: str = ""
    homebrew_installed: bool = False
    homebrew_prefix: str = ""
    xcode_cli_installed: bool = False

@dataclass
class AuditReport:
    timestamp: str
    system: SystemInfo
    tools: list[ToolStatus] = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    drift: Optional[dict] = None

def run_command(cmd: str, timeout: int = 10) -> tuple[int, str]:
    """Run a shell command and return (exit_code, output)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, "timeout"
    except Exception as e:
        return -1, str(e)

def get_system_info() -> SystemInfo:
    """Gather basic system information."""
    info = SystemInfo()

    # Hostname
    code, out = run_command("hostname -s")
    info.hostname = out if code == 0 else "unknown"

    # macOS version
    code, out = run_command("sw_vers -productVersion")
    info.macos_version = out if code == 0 else "unknown"

    # Architecture
    code, out = run_command("uname -m")
    info.architecture = out if code == 0 else "unknown"

    # Default shell
    info.shell = os.environ.get("SHELL", "/bin/zsh")

    # Homebrew
    code, out = run_command("command -v brew")
    info.homebrew_installed = code == 0
    if info.homebrew_installed:
        code, out = run_command("brew --prefix")
        info.homebrew_prefix = out if code == 0 else ""

    # Xcode CLI tools
    code, _ = run_command("xcode-select -p")
    info.xcode_cli_installed = code == 0

    return info

def get_version(task: dict) -> Optional[str]:
    """Try to get version for an installed tool."""
    version_cmd = task.get('detection', {}).get('version_command')
    if version_cmd:
        code, out = run_command(version_cmd, timeout=5)
        if code == 0 and out:
            # Extract first line, trim common prefixes
            version = out.split('\n')[0]
            for prefix in ['v', 'version ', 'Version ']:
                if version.lower().startswith(prefix.lower()):
                    version = version[len(prefix):]
            return version[:50]  # Limit length
    return None

def get_install_path(task: dict) -> Optional[str]:
    """Try to determine install path for a tool."""
    detection = task.get('detection', {})

    # Check for app bundle
    indicator = detection.get('installed_indicator')
    if indicator and indicator.startswith('/Applications'):
        if os.path.exists(indicator):
            return indicator

    # Check command path
    check_cmd = detection.get('check_command', '')
    if 'command -v' in check_cmd:
        # Extract the command name
        parts = check_cmd.split('command -v')
        if len(parts) > 1:
            cmd_name = parts[1].strip().split()[0]
            code, out = run_command(f"command -v {cmd_name}")
            if code == 0:
                return out

    return None

def check_tool(task_id: str, task: dict, quick: bool = False) -> ToolStatus:
    """Check installation status of a single tool."""
    detection = task.get('detection', {})
    check_cmd = detection.get('check_command')

    status = ToolStatus(
        task_id=task_id,
        name=task.get('name', task_id),
        category=task.get('category', 'unknown'),
        installed=False,
        detection_method=check_cmd[:60] if check_cmd else "(none)"
    )

    if not check_cmd:
        status.error = "No detection command"
        return status

    code, _ = run_command(check_cmd)
    status.installed = code == 0

    if status.installed and not quick:
        status.version = get_version(task)
        status.install_path = get_install_path(task)

    return status

def load_tasks(category: Optional[str] = None) -> dict:
    """Load task definitions from YAML manifests."""
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    tasks = {}
    core_dir = PROJECT_ROOT / 'tasks/core'

    if category:
        manifests = [core_dir / f"{category}.yaml"]
        manifests = [m for m in manifests if m.exists()]
    else:
        manifests = list(core_dir.glob('*.yaml'))

    for manifest in manifests:
        with open(manifest) as f:
            data = yaml.safe_load(f)
        if data and 'tasks' in data:
            for task_id, task in data['tasks'].items():
                task['category'] = manifest.stem
                tasks[task_id] = task

    return tasks

def run_audit(category: Optional[str] = None, quick: bool = False, parallel: bool = True) -> AuditReport:
    """Run full system audit."""
    report = AuditReport(
        timestamp=datetime.now().isoformat(),
        system=get_system_info()
    )

    tasks = load_tasks(category)

    if parallel and not quick:
        # Run checks in parallel for speed
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(check_tool, tid, task, quick): tid
                for tid, task in tasks.items()
            }
            for future in concurrent.futures.as_completed(futures):
                report.tools.append(future.result())
    else:
        # Sequential execution
        for task_id, task in tasks.items():
            report.tools.append(check_tool(task_id, task, quick))

    # Sort by category then name
    report.tools.sort(key=lambda t: (t.category, t.name))

    # Generate summary
    installed = [t for t in report.tools if t.installed]
    not_installed = [t for t in report.tools if not t.installed and not t.error]
    errors = [t for t in report.tools if t.error]

    by_category = {}
    for tool in report.tools:
        cat = tool.category
        if cat not in by_category:
            by_category[cat] = {'installed': 0, 'total': 0}
        by_category[cat]['total'] += 1
        if tool.installed:
            by_category[cat]['installed'] += 1

    report.summary = {
        'total_tools': len(report.tools),
        'installed': len(installed),
        'not_installed': len(not_installed),
        'errors': len(errors),
        'by_category': by_category
    }

    return report

def compare_with_session(report: AuditReport, session_path: str) -> dict:
    """Compare current state with a previous session."""
    with open(session_path) as f:
        session = json.load(f)

    # Extract installed tools from session
    session_tools = set()
    for task in session.get('completed_tasks', []):
        session_tools.add(task.get('task_id', task.get('id', '')))

    # Compare
    current_installed = {t.task_id for t in report.tools if t.installed}

    drift = {
        'added_outside_session': list(current_installed - session_tools),
        'removed_since_session': list(session_tools - current_installed),
        'still_installed': list(current_installed & session_tools)
    }

    return drift

def print_human_report(report: AuditReport):
    """Print human-readable report."""
    print("=" * 70)
    print("AGENTIC PROVISION - SYSTEM AUDIT REPORT")
    print("=" * 70)
    print(f"Timestamp: {report.timestamp}")
    print()

    # System info
    print("SYSTEM INFORMATION")
    print("-" * 40)
    print(f"  Hostname:        {report.system.hostname}")
    print(f"  macOS:           {report.system.macos_version}")
    print(f"  Architecture:    {report.system.architecture}")
    print(f"  Shell:           {report.system.shell}")
    print(f"  Homebrew:        {'✓ ' + report.system.homebrew_prefix if report.system.homebrew_installed else '✗ Not installed'}")
    print(f"  Xcode CLI:       {'✓ Installed' if report.system.xcode_cli_installed else '✗ Not installed'}")
    print()

    # Summary
    print("SUMMARY")
    print("-" * 40)
    s = report.summary
    print(f"  Total tools checked:  {s['total_tools']}")
    print(f"  Installed:            {s['installed']}")
    print(f"  Not installed:        {s['not_installed']}")
    if s['errors']:
        print(f"  Detection errors:     {s['errors']}")
    print()

    # By category
    print("BY CATEGORY")
    print("-" * 40)
    for cat, counts in sorted(s['by_category'].items()):
        bar_len = int((counts['installed'] / max(counts['total'], 1)) * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"  {cat:20} {bar} {counts['installed']}/{counts['total']}")
    print()

    # Installed tools
    installed = [t for t in report.tools if t.installed]
    if installed:
        print("INSTALLED TOOLS")
        print("-" * 40)
        current_cat = None
        for tool in installed:
            if tool.category != current_cat:
                current_cat = tool.category
                print(f"\n  [{current_cat}]")
            version_str = f" ({tool.version})" if tool.version else ""
            print(f"    ✓ {tool.name}{version_str}")
    print()

    # Drift info if present
    if report.drift:
        print("DRIFT FROM SESSION")
        print("-" * 40)
        if report.drift['added_outside_session']:
            print("  Added outside session:")
            for t in report.drift['added_outside_session']:
                print(f"    + {t}")
        if report.drift['removed_since_session']:
            print("  Removed since session:")
            for t in report.drift['removed_since_session']:
                print(f"    - {t}")
        print()

    print("=" * 70)

def print_json_report(report: AuditReport):
    """Print machine-readable JSON report."""
    output = {
        'timestamp': report.timestamp,
        'system': asdict(report.system),
        'tools': [asdict(t) for t in report.tools],
        'summary': report.summary
    }
    if report.drift:
        output['drift'] = report.drift

    print(json.dumps(output, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description='Audit system for installed development tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./audit-system.py                     Full audit, human-readable
  ./audit-system.py --json              Machine-readable JSON
  ./audit-system.py --category editors  Audit only editors
  ./audit-system.py --quick             Fast audit (skip versions)
  ./audit-system.py --diff session.json Compare against session
        """
    )
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--category', type=str,
                        help='Audit specific category only')
    parser.add_argument('--quick', action='store_true',
                        help='Quick audit (skip version detection)')
    parser.add_argument('--diff', type=str, metavar='SESSION',
                        help='Compare against session state file')
    parser.add_argument('--no-parallel', action='store_true',
                        help='Disable parallel execution')
    parser.add_argument('--output', '-o', type=str,
                        help='Write report to file')

    args = parser.parse_args()

    # Run audit
    report = run_audit(
        category=args.category,
        quick=args.quick,
        parallel=not args.no_parallel
    )

    # Compare with session if requested
    if args.diff:
        if os.path.exists(args.diff):
            report.drift = compare_with_session(report, args.diff)
        else:
            print(f"Warning: Session file not found: {args.diff}", file=sys.stderr)

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            if args.json:
                json.dump({
                    'timestamp': report.timestamp,
                    'system': asdict(report.system),
                    'tools': [asdict(t) for t in report.tools],
                    'summary': report.summary,
                    'drift': report.drift
                }, f, indent=2)
            else:
                # Redirect stdout temporarily
                old_stdout = sys.stdout
                sys.stdout = f
                print_human_report(report)
                sys.stdout = old_stdout
        print(f"Report written to: {args.output}")
    else:
        if args.json:
            print_json_report(report)
        else:
            print_human_report(report)

if __name__ == '__main__':
    main()
