#!/usr/bin/env python3
"""Validate task manifest schema compliance."""

import yaml
import sys
from pathlib import Path

REQUIRED_TASK_FIELDS = ['id', 'name', 'description', 'install']
REQUIRED_INSTALL_FIELDS = ['steps']

def validate_task(task_id: str, task: dict, filepath: str) -> list[str]:
    """Validate a single task definition."""
    errors = []

    # Check required fields
    for field in REQUIRED_TASK_FIELDS:
        if field not in task:
            errors.append(f"{filepath}: Task '{task_id}' missing required field '{field}'")

    # Validate install section
    if 'install' in task:
        install = task['install']
        if 'steps' not in install:
            errors.append(f"{filepath}: Task '{task_id}' install section missing 'steps'")
        elif not isinstance(install['steps'], list):
            errors.append(f"{filepath}: Task '{task_id}' install.steps must be a list")
        else:
            for i, step in enumerate(install['steps']):
                if 'command' not in step:
                    errors.append(f"{filepath}: Task '{task_id}' step {i} missing 'command'")

    # Validate detection section if present
    if 'detection' in task:
        detection = task['detection']
        if 'check_command' not in detection and 'installed_indicator' not in detection:
            errors.append(f"{filepath}: Task '{task_id}' detection needs check_command or installed_indicator")

    # Validate ID matches key
    if 'id' in task and task['id'] != task_id:
        errors.append(f"{filepath}: Task key '{task_id}' doesn't match id field '{task['id']}'")

    return errors

def validate_manifest(filepath: Path) -> list[str]:
    """Validate a task manifest file."""
    errors = []

    with open(filepath) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return [f"{filepath}: Invalid YAML - {e}"]

    if data is None:
        return [f"{filepath}: Empty file"]

    if 'tasks' not in data:
        return [f"{filepath}: Missing 'tasks' key"]

    for task_id, task in data['tasks'].items():
        errors.extend(validate_task(task_id, task, str(filepath)))

    return errors

def validate_profile(filepath: Path) -> list[str]:
    """Validate a profile manifest file."""
    errors = []

    with open(filepath) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return [f"{filepath}: Invalid YAML - {e}"]

    if data is None:
        return [f"{filepath}: Empty file"]

    if 'metadata' not in data:
        errors.append(f"{filepath}: Missing 'metadata' section")
    else:
        metadata = data['metadata']
        for field in ['id', 'name', 'description']:
            if field not in metadata:
                errors.append(f"{filepath}: Missing metadata.{field}")

    if 'question_flow' not in data:
        errors.append(f"{filepath}: Missing 'question_flow' section")
    else:
        for i, question in enumerate(data['question_flow']):
            if 'id' not in question:
                errors.append(f"{filepath}: Question {i} missing 'id'")
            if 'question' not in question:
                errors.append(f"{filepath}: Question {i} missing 'question'")
            if 'options' not in question:
                errors.append(f"{filepath}: Question {i} missing 'options'")
            else:
                for j, opt in enumerate(question['options']):
                    if 'letter' not in opt:
                        errors.append(f"{filepath}: Question {i} option {j} missing 'letter'")
                    if 'text' not in opt:
                        errors.append(f"{filepath}: Question {i} option {j} missing 'text'")

    return errors

def check_duplicate_task_ids(manifests: list[Path]) -> list[str]:
    """Check for duplicate task IDs across all manifests."""
    errors = []
    all_ids = {}

    for manifest in manifests:
        with open(manifest) as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError:
                continue

        if data and 'tasks' in data:
            for task_id in data['tasks'].keys():
                if task_id in all_ids:
                    errors.append(f"Duplicate task ID '{task_id}' in {manifest} (also in {all_ids[task_id]})")
                else:
                    all_ids[task_id] = manifest

    return errors

def main():
    errors = []

    # Find project root (where tasks/ directory is)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Validate core tasks
    core_manifests = list((project_root / 'tasks/core').glob('*.yaml'))
    print(f"Validating {len(core_manifests)} core task manifests...")

    for manifest in core_manifests:
        manifest_errors = validate_manifest(manifest)
        errors.extend(manifest_errors)
        if not manifest_errors:
            print(f"  ✓ {manifest.name}")
        else:
            print(f"  ✗ {manifest.name} ({len(manifest_errors)} errors)")

    # Check for duplicate IDs
    dup_errors = check_duplicate_task_ids(core_manifests)
    errors.extend(dup_errors)

    # Validate profiles
    profile_manifests = list((project_root / 'tasks/profiles').glob('*.yaml'))
    print(f"\nValidating {len(profile_manifests)} profile manifests...")

    for profile in profile_manifests:
        profile_errors = validate_profile(profile)
        errors.extend(profile_errors)
        if not profile_errors:
            print(f"  ✓ {profile.name}")
        else:
            print(f"  ✗ {profile.name} ({len(profile_errors)} errors)")

    # Summary
    print(f"\n{'='*60}")
    if errors:
        print(f"Validation FAILED: {len(errors)} error(s) found")
        print()
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Validation PASSED: All manifests valid")
        sys.exit(0)

if __name__ == '__main__':
    main()
