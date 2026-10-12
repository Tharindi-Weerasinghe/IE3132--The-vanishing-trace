#!/usr/bin/env python3
"""Read-only audit helper for a SAVED sudo -l text file from an isolated lab.

It does not run sudo, change permissions or exploit a target.
"""
from pathlib import Path
import argparse
import re

def assess(text):
    matches=[]
    for line in text.splitlines():
        if 'NOPASSWD' in line and re.search(r'(?:^|[\s,/])(?:/usr/bin/)?find(?:\s|$)',line):
            matches.append(line.strip())
    return matches

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Read saved permission output; does not connect to a VM')
    p.add_argument('file',help='Text file holding reviewed sudo -l output')
    args=p.parse_args();hits=assess(Path(args.file).read_text())
    if hits:
        print('REVIEW NEEDED: privileged find rule:',*hits,sep='\n- ')
    else:print('No NOPASSWD find rule found in the supplied text.')
