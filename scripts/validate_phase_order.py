#!/usr/bin/env python3
"""Validate that BUILD-STATUS.md part completions respect phase dependency order."""
import os, re, subprocess, sys

PHASES = [
    {1, 2, 3},      # Phase 1
    {4, 5},          # Phase 2
    {6, 7, 8},       # Phase 3
    {9, 10, 11, 12}, # Phase 4
    {13, 14, 15, 16, 17, 18},  # Phase 5
]

def phase_of(part):
    for i, phase in enumerate(PHASES):
        if part in phase:
            return i
    return -1

def parse_status(content):
    done, pending = set(), set()
    for m in re.finditer(r'(✅|⬜)\s*\|\s*(\d+)', content):
        (done if m.group(1) == '✅' else pending).add(int(m.group(2)))
    return done, pending

def main():
    base = os.environ.get('GITHUB_BASE_REF', 'main')
    head = os.environ.get('GITHUB_HEAD_REF', 'HEAD')

    try:
        old = subprocess.check_output(['git', 'show', f'origin/{base}:BUILD-STATUS.md'], text=True)
    except subprocess.CalledProcessError:
        print("No BUILD-STATUS.md on base — skipping.")
        return 0
    try:
        new = subprocess.check_output(['git', 'show', f'origin/{head}:BUILD-STATUS.md'], text=True)
    except subprocess.CalledProcessError:
        print("No BUILD-STATUS.md on head — skipping.")
        return 0

    old_done, _ = parse_status(old)
    new_done, _ = parse_status(new)
    newly_completed = new_done - old_done
    if not newly_completed:
        print("No new completions — skipping.")
        return 0

    violations = []
    for part in newly_completed:
        phase = phase_of(part)
        if phase <= 0:
            continue
        prereqs = PHASES[phase - 1]
        missing = prereqs - new_done
        if missing:
            violations.append(f"Part {part} (phase {phase+1}) requires parts {sorted(missing)} from phase {phase}")

    if violations:
        print("❌ Phase dependency violations:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(f"✅ {len(newly_completed)} new completions respect phase order.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
