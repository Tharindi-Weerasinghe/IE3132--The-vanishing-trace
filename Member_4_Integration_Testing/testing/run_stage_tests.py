#!/usr/bin/env python3
"""Run included source-level stage tests. Not a CTFd end-to-end certification.
Each test is executed in its stage directory and timed out after 25 seconds.
Records real output; missing Scapy/steghide remains a missing test dependency.
"""
from pathlib import Path
import argparse
import datetime
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
STAGES=sorted((ROOT/'challenges').glob('stage0?-*'))

def run(timeout=25):
    data={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'note':'Unit/source tests only. Not live VM/CTFd submission or isolation evidence.',
          'stages':[]}
    for folder in STAGES:
        cmd=[sys.executable,'test_challenge.py']
        try:
            test=subprocess.run(cmd,cwd=str(folder),capture_output=True,text=True,
                                timeout=timeout,check=False)
            out=(test.stdout+'\n'+test.stderr)[-5000:]
            state='passed' if test.returncode==0 else 'failed'
            if state=='passed' and ('skipped=2' in out or 'SKIP' in out.upper()):
                state='passed_with_skips'
            data['stages'].append({'stage':folder.name,'status':state,
                                    'exit_code':test.returncode,'output':out})
        except subprocess.TimeoutExpired:
            data['stages'].append({'stage':folder.name,'status':'timed_out',
                                    'output':f'Test exceeded {timeout} seconds'})
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--json',dest='path',help='Save actual test output to JSON (review before sharing)')
    args=parser.parse_args();result=run()
    for item in result['stages']:
        print(f"{item['stage']}: {item['status']}")
    if args.path:
        Path(args.path).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print('Saved actual run output:',args.path)
    if any(x['status'] in ('failed','timed_out') for x in result['stages']):
        raise SystemExit(1)
