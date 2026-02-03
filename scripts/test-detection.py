#!/usr/bin/env python3
"""
Test detection commands without installing anything.
Safe to run on any machine.
"""

import yaml
import subprocess
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class DetectionResult:
    task_id: str
    check_command: str
    detected: bool
    error: Optional[str] = None
    is_formula: bool = False  # vs cask

def test_detection(task_id: str, task: dict) -> DetectionResult:
    """Test a single detection command."""
    detection = task.get('detection', {})
    check_cmd = detection.get('check_command')

    if not check_cmd:
        return DetectionResult(
            task_id=task_id,
            check_command="(none)",
            detected=False,
            error="No detection command"
        )

    # Determine if formula or cask
    install_steps = task.get('install', {}).get('steps', [])
    install_cmd = install_steps[0].get('command', '') if install_steps else ''
    is_formula = '--cask' not in install_cmd

    try:
        result = subprocess.run(
            check_cmd,
            shell=True,
            capture_output=True,
            timeout=10
        )
        return DetectionResult(
            task_id=task_id,
            check_command=check_cmd[:60] + ('...' if len(check_cmd) > 60 else ''),
            detected=result.returncode == 0,
            is_formula=is_formula
        )
    except subprocess.TimeoutExpired:
        return DetectionResult(
            task_id=task_id,
            check_command=check_cmd[:60],
            detected=False,
            error="Timeout",
            is_formula=is_formula
        )
    except Exception as e:
        return DetectionResult(
            task_id=task_id,
            check_command=check_cmd[:60],
            detected=False,
            error=str(e)[:50],
            is_formula=is_formula
        )

def main():
    parser = argparse.ArgumentParser(description='Test task detection commands')
    parser.add_argument('--formulas-only', action='store_true',
                        help='Only test Homebrew formulas (for Docker)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all results, not just errors')
    parser.add_argument('--category', type=str,
                        help='Test only specific category (e.g., cli-tools)')
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    results = []

    # Find manifest files
    if args.category:
        manifests = [project_root / f"tasks/core/{args.category}.yaml"]
        manifests = [m for m in manifests if m.exists()]
    else:
        manifests = list((project_root / 'tasks/core').glob('*.yaml'))

    if not manifests:
        print(f"No manifests found", file=sys.stderr)
        sys.exit(1)

    for manifest in sorted(manifests):
        with open(manifest) as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Error parsing {manifest}: {e}", file=sys.stderr)
                continue

        if not data or 'tasks' not in data:
            continue

        category = manifest.stem

        if not args.json:
            print(f"\n{'='*60}")
            print(f"Category: {category}")
            print('='*60)

        for task_id, task in data.get('tasks', {}).items():
            result = test_detection(task_id, task)

            # Skip casks in formula-only mode
            if args.formulas_only and not result.is_formula:
                continue

            results.append({
                'category': category,
                'task_id': result.task_id,
                'detected': result.detected,
                'error': result.error,
                'is_formula': result.is_formula
            })

            if not args.json:
                # Display result
                if result.error and result.error != "No detection command":
                    print(f"  ⚠ {task_id}: ERROR - {result.error}")
                elif result.detected:
                    if args.verbose:
                        print(f"  ✓ {task_id}: detected")
                else:
                    if args.verbose:
                        print(f"  ○ {task_id}: not installed")

    # Output JSON if requested
    if args.json:
        import json
        print(json.dumps(results, indent=2))
        sys.exit(0)

    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print('='*60)

    detected = [r for r in results if r['detected']]
    not_detected = [r for r in results if not r['detected'] and not r['error']]
    no_detection = [r for r in results if r['error'] == "No detection command"]
    errors = [r for r in results if r['error'] and r['error'] != "No detection command"]

    print(f"  Detected (installed):     {len(detected)}")
    print(f"  Not detected:             {len(not_detected)}")
    print(f"  No detection command:     {len(no_detection)}")
    print(f"  Errors:                   {len(errors)}")
    print(f"  Total tasks:              {len(results)}")

    if errors:
        print("\nDetection errors:")
        for r in errors:
            print(f"  - {r['task_id']}: {r['error']}")
        sys.exit(1)

    if no_detection and args.verbose:
        print("\nTasks without detection commands:")
        for r in no_detection:
            print(f"  - {r['task_id']}")

    sys.exit(0)

if __name__ == '__main__':
    main()
