#!/usr/bin/env python3
"""Offline organizer solver, using only the PCAP and its protocol content."""
import argparse
import base64
import json
from pathlib import Path
import re
from scapy.all import rdpcap,IP,TCP

def streams(path):
    flows={}
    for p in rdpcap(str(path)):
        if IP not in p or TCP not in p:continue
        data=bytes(p[TCP].payload)
        if not data:continue
        key=(p[IP].src,p[TCP].sport,p[IP].dst,p[TCP].dport)
        positions=flows.setdefault(key,{})
        for offset,value in enumerate(data):
            seq=int(p[TCP].seq)+offset
            if seq in positions and positions[seq]!=value:raise ValueError("Conflicting retransmission")
            positions[seq]=value
    result={}
    for key,positions in flows.items():
        low,high=min(positions),max(positions)
        if len(positions)!=high-low+1:raise ValueError("Missing stream bytes")
        result[key]=bytes(positions[n] for n in range(low,high+1))
    return result

def recover(path):
    matches=[]
    for endpoints,data in streams(path).items():
        if not data.startswith(b"POST /sync/notes HTTP/1.1\r\n"):continue
        headers,body=data.split(b"\r\n\r\n",1)
        length=int(re.search(br"Content-Length: (\d+)",headers).group(1))
        if len(body)!=length:raise ValueError("HTTP body length mismatch")
        obj=json.loads(body)
        parts=sorted(obj["parts"],key=lambda p:p["seq"])
        if [p["seq"] for p in parts]!=list(range(1,len(parts)+1)):raise ValueError("Invalid part sequence")
        note=base64.b64decode("".join(p["data"] for p in parts),validate=True).decode()
        flags=re.findall(r"TVT\{[a-z0-9_]+\}",note)
        if len(flags)!=1:raise ValueError("Expected one receipt")
        matches.append((endpoints,note,flags[0]))
    if len(matches)!=1:raise ValueError("Expected one relevant conversation")
    return matches[0]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("pcap",nargs="?",type=Path,default=Path(__file__).resolve().parent/"dist/silent-connection.pcap")
    endpoints,note,flag=recover(p.parse_args().pcap)
    print("Endpoints:",endpoints);print(note)

if __name__=="__main__":main()
