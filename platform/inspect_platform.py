#!/usr/bin/env python3
"""Read-only evidence collection helper on the course CTFd-Host Linux VM.

Reports local command output for manual review. Does not infer that a network
is isolated merely because an IP is private; inspect hypervisor network settings.
This is newly drafted support code, NOT evidence of Member 1's actual setup.
"""
import argparse
import datetime
import json
import shutil
import subprocess

COMMANDS={
    'host_addresses': ['ip','-j','address','show'],
    'host_routes': ['ip','route','show'],
    'running_containers': ['docker','ps','--format','{{json .}}'],
}

def analyze_routes(output):
    lines=output.splitlines()
    return {'default_route_present': any(line.lstrip().startswith('default ') for line in lines),
            'route_lines': len(lines),
            'warning': 'Default route found: manually review whether it reaches an external network.'
                if any(line.lstrip().startswith('default ') for line in lines)
                else 'No default route in collected output. Still verify the hypervisor adapter configuration.'}

def collect(timeout=5):
    result={'collected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'note':'Read-only local output, NOT verification of isolation or correct deployment.',
            'commands':{}}
    for title,cmd in COMMANDS.items():
        if shutil.which(cmd[0]) is None:
            result['commands'][title]={'status':'unavailable','reason':cmd[0]+' not installed'}
            continue
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
            result['commands'][title]={'status':'finished','exit_code':p.returncode,
                                       'stdout':p.stdout[:30000],'stderr':p.stderr[:3000]}
        except (OSError,subprocess.TimeoutExpired) as ex:
            result['commands'][title]={'status':'error','error':str(ex)}
    route=result['commands'].get('host_routes',{})
    if route.get('status')=='finished':result['route_review']=analyze_routes(route.get('stdout',''))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Collect read-only local CTFd host environment information')
    p.add_argument('--output',help='Optional report destination (do not publish without reviewing for sensitive data)')
    args=p.parse_args();result=json.dumps(collect(),indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(result+'\n',encoding='utf-8')
        print('Wrote local report:',args.output)
    else:print(result)
