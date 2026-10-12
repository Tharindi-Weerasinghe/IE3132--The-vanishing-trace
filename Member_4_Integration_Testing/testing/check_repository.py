#!/usr/bin/env python3
"""Non-invasive repository structure and flag-convention audit."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
stages=sorted((ROOT/'challenges').glob('stage0?-*'))
issues=[]
print(f'Found {len(stages)} stage folders')
if len(stages)!=6:issues.append(f'Expected 6, got {len(stages)}')
for folder in stages:
    files={p.name for p in folder.iterdir() if p.is_file()}
    print(f'  {folder.name}: {len(files)} top-level files')
    if 'README.md' not in files:issues.append(f'{folder.name}: README.md missing')
    if 'CTFD-SETUP.md' not in files:issues.append(f'{folder.name}: CTFD-SETUP.md missing')
    if 'test_challenge.py' not in files:issues.append(f'{folder.name}: test_challenge.py missing')
    md=(folder/'CTFD-SETUP.md')
    if md.exists():
        flags=set(re.findall(r'\b(?:LTX|TVT)\{[^}]+\}',md.read_text()))
        if flags:
            prefixes={f.split('{')[0] for f in flags}
            print('    Organizer prefix:',', '.join(sorted(prefixes)))
            if prefixes!={'LTX'}: issues.append(f'{folder.name}: flag prefix differs from briefing LTX')
for problem in issues:print('REVIEW REQUIRED:',problem)
print('This is a repository audit, NOT a CTFd integration test.')
raise SystemExit(bool(issues))
