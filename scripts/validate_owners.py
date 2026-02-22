#!/usr/bin/env python3
"""Validate that changed files in a PR belong to the branch's owned or shared paths."""
import fnmatch, json, os, subprocess, sys, yaml

def load_owners():
    with open(os.path.join(os.path.dirname(__file__), '..', '.github', 'OWNERS.yaml')) as f:
        return yaml.safe_load(f)

def changed_files():
    base = os.environ.get('GITHUB_BASE_REF', 'main')
    head = os.environ.get('GITHUB_HEAD_REF', 'HEAD')
    out = subprocess.check_output(['git', 'diff', '--name-only', f'origin/{base}...origin/{head}'], text=True)
    return [f for f in out.strip().split('\n') if f]

def matches_any(path, patterns):
    return any(fnmatch.fnmatch(path, p) for p in patterns)

def main():
    owners = load_owners()
    branch = os.environ.get('GITHUB_HEAD_REF', '')
    files = changed_files()
    if not branch or not files:
        print("No branch or no changed files — skipping.")
        return 0

    allowed = owners.get('lanes', {}).get(branch, [])
    shared = owners.get('shared', [])
    if not allowed:
        print(f"Branch '{branch}' has no lane in OWNERS.yaml — all files allowed.")
        return 0

    violations = [f for f in files if not matches_any(f, allowed + shared)]
    if violations:
        print(f"❌ Ownership violation on branch '{branch}':")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"✅ All {len(files)} changed files are within owned/shared paths.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
