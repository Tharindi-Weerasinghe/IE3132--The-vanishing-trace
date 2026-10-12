#!/usr/bin/env python3
"""Reference request to intentionally vulnerable synthetic lab; restricted to private IPs."""
import argparse
import ipaddress
import json
from urllib.parse import urlparse
from urllib.request import urlopen

def solve(base):
    parsed=urlparse(base)
    if parsed.scheme!='http' or not parsed.hostname:raise ValueError('Use http URL for local lab')
    ip=ipaddress.ip_address(parsed.hostname)
    if not (ip.is_loopback or ip in ipaddress.ip_network('192.168.128.0/24')):
        raise ValueError('For isolated local lab targets only')
    with urlopen(base.rstrip('/')+'/record/7',timeout=3) as r:
        return json.loads(r.read().decode())['content']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:5000')
    print(solve(p.parse_args().url))
