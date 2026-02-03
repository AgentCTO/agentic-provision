#!/usr/bin/env python3
"""Validate that all task references in profiles exist in core manifests."""

import yaml
import sys
from pathlib import Path

def load_all_task_ids(core_dir: Path) -> set[str]:
    """Load all task IDs from core manifests."""
    task_ids = set()

    for manifest in core_dir.glob('*.yaml'):
        with open(manifest) as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError:
                continue

        if data and 'tasks' in data:
            task_ids.update(data['tasks'].keys())

    return task_ids

def validate_profile_refs(profile_path: Path, valid_task_ids: set[str]) -> list[str]:
    """Validate all task references in a profile."""
    errors = []

    with open(profile_path) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return [f"{profile_path}: Invalid YAML - {e}"]

    if not data:
        return []

    # Check required_tasks
    for task_id in data.get('required_tasks', []):
        if task_id not in valid_task_ids:
            errors.append(f"{profile_path}: required_tasks references unknown task '{task_id}'")

    # Check question_flow options
    for question in data.get('question_flow', []):
        q_id = question.get('id', 'unknown')
        for option in question.get('options', []):
            for task_id in option.get('tasks', []):
                if task_id not in valid_task_ids:
                    errors.append(f"{profile_path}: question '{q_id}' references unknown task '{task_id}'")

    # Check default_cli_tools
    for task_id in data.get('default_cli_tools', []):
        if task_id not in valid_task_ids:
            errors.append(f"{profile_path}: default_cli_tools references unknown task '{task_id}'")

    # Check post_install_suggestions
    for task_id in data.get('post_install_suggestions', []):
        if task_id not in valid_task_ids:
            errors.append(f"{profile_path}: post_install_suggestions references unknown task '{task_id}'")

    return errors

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    core_dir = project_root / 'tasks/core'
    profiles_dir = project_root / 'tasks/profiles'

    # Load all valid task IDs
    print("Loading task IDs from core manifests...")
    valid_task_ids = load_all_task_ids(core_dir)
    print(f"  Found {len(valid_task_ids)} task definitions")

    # Validate each profile
    errors = []
    print("\nValidating profile references...")

    for profile in profiles_dir.glob('*.yaml'):
        profile_errors = validate_profile_refs(profile, valid_task_ids)
        errors.extend(profile_errors)

        if not profile_errors:
            print(f"  ✓ {profile.name}")
        else:
            print(f"  ✗ {profile.name} ({len(profile_errors)} missing references)")

    # Summary
    print(f"\n{'='*60}")
    if errors:
        print(f"Validation FAILED: {len(errors)} missing reference(s)")
        print()
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Validation PASSED: All profile references valid")
        sys.exit(0)

if __name__ == '__main__':
    main()
