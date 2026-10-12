#!/usr/bin/env python3
"""Write synthetic packets to disk only. No capture, sniffing or transmission."""
import base64
from datetime import datetime,timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from scapy.all import Ether,IP,UDP,TCP,DNS,DNSQR,DNSRR,Raw,wrpcap
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parent
FLAG="TVT{the_stream_kept_the_last_word}"
NOTE=("Mira's transfer receipt\n2026-09-29 09:17:33 UTC\n"
      "The collection copy survived. My final account is held on the separate terminal.\n"
      "This receipt completes the connection evidence: "+FLAG+"\n")
START=int(datetime(2026,9,29,9,17,tzinfo=timezone.utc).timestamp())
PACKETS=[]

def emit(packet,seconds):
    # Parse serialized bytes to materialize lengths and checksums before writing.
    p=Ether(bytes(packet));p.time=Decimal(START)+Decimal(str(seconds));PACKETS.append(p)

def eth(reverse=False):
    a,b="02:00:00:00:00:10","02:00:00:00:00:01"
    return Ether(src=b if reverse else a,dst=a if reverse else b)

def dns(client,host,server,index,start):
    q=DNSQR(qname=host)
    emit(eth()/IP(src=client,dst="192.0.2.53")/UDP(sport=53000+index,dport=53)/DNS(id=1000+index,rd=1,qd=q),start)
    emit(eth(True)/IP(src="192.0.2.53",dst=client)/UDP(sport=53,dport=53000+index)/DNS(id=1000+index,qr=1,aa=1,rd=1,ra=1,qd=q,an=DNSRR(rrname=host,ttl=60,rdata=server)),start+.01)

def flow(client,server,sport,index,start,request,response,retransmit=False):
    c=100000+index*10000;s=900000+index*10000;t=start
    def add(direction,flags,seq,ack,data=b""):
        nonlocal t
        src,dst=(server,client) if direction else (client,server)
        sp,dp=(80,sport) if direction else (sport,80)
        packet=eth(direction)/IP(src=src,dst=dst,id=100+index)/TCP(sport=sp,dport=dp,seq=seq,ack=ack,flags=flags,window=64240)
        if data:packet=packet/Raw(data)
        emit(packet,t);t=round(t+.01,6)
    add(False,"S",c,0);c+=1
    add(True,"SA",s,c);s+=1
    add(False,"A",c,s)
    for n in range(0,len(request),113):
        part=request[n:n+113]
        add(False,"PA",c,s,part);old=c;c+=len(part)
        add(True,"A",s,c)
        if retransmit and n==226:
            add(False,"PA",old,s,part);add(True,"A",s,c)
    for n in range(0,len(response),97):
        part=response[n:n+97]
        add(True,"PA",s,c,part);s+=len(part);add(False,"A",c,s)
    add(False,"FA",c,s);c+=1;add(True,"A",s,c)
    add(True,"FA",s,c);s+=1;add(False,"A",c,s)

def main():
    PACKETS.clear()
    for i in range(24):
        client="192.0.2.10" if i%3!=0 else "192.0.2.11"
        host="catalogue.mira.test" if i%2==0 else "weather.mira.test"
        server="192.0.2.20" if i%2==0 else "192.0.2.21"
        method="GET";path="/catalogue?page="+str(i);body=b""
        if i==11:
            client="192.0.2.10";host="relay.mira.test";server="198.51.100.77"
            method="POST";path="/sync/notes"
            encoded=base64.b64encode(NOTE.encode()).decode()
            size=((len(encoded)+3)//4+3)//4*4
            chunks=[encoded[n:n+size] for n in range(0,len(encoded),size)]
            assert len(chunks)==4
            parts=[{"seq":n+1,"data":chunk} for n,chunk in enumerate(chunks)]
            body=json.dumps({"record":"collection-copy","encoding":"base64",
                "assembly":"Join data fields in ascending seq order, then decode.",
                "parts":[parts[n] for n in (2,0,3,1)]},separators=(",",":")).encode()
        elif i in (5,18):
            method="POST";path="/metrics"
            body=json.dumps({"sensor":"humidity","value":61+i,"unit":"percent"}).encode()
        request=(f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: MiraResearchClient/1.0\r\n"
                 "Content-Type: application/json\r\n"+f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode()+body
        reply=json.dumps({"status":"stored" if i==11 else "ok","record_count":1 if i==11 else i+4}).encode()
        response=("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                  f"Content-Length: {len(reply)}\r\nConnection: close\r\n\r\n").encode()+reply
        dns(client,host,server,i,i*3)
        flow(client,server,41000+i,i,i*3+.1,request,response,retransmit=i==11)
    out=ROOT/"dist";out.mkdir(exist_ok=True)
    pcap=out/"silent-connection.pcap"
    wrpcap(str(pcap),sorted(PACKETS,key=lambda p:p.time))
    brief=b"""THE VANISHING TRACE / CASE PACKET 05 / THE SILENT CONNECTION
This capture is synthetic. Analyze it offline; no connection to any host is needed.
All capture timestamps are UTC. Mira's workstation is 192.0.2.10.
A collection-copy transfer was reported between 09:17:30 and 09:17:40 UTC on
2026-09-29. Routine catalogue and weather traffic was active around it.

Identify the relevant endpoint and conversation. Follow its complete TCP stream,
then reconstruct the application message according to its own sequence fields.
TCP packet boundaries and application record order are different things.
Recover and submit the transfer receipt. No earlier challenge flag is required.

The .test names and documentation IP ranges are fictional identifiers, not live
targets. The file contains generated DNS, TCP and HTTP packets only.
"""
    player=out/"stage05-evidence.zip"
    with ZipFile(player,"w",ZIP_DEFLATED) as z:
        for name,data in [("START-HERE.txt",brief),(pcap.name,pcap.read_bytes())]:
            info=ZipInfo(name,(2026,9,29,9,20,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,data)
    (out/"SHA256SUMS.txt").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name+"\n" for p in (player,pcap)))
    print(f"Wrote {len(PACKETS)} synthetic packets across 24 TCP conversations.")
    print(f"PLAYER FILE: {player}\nNext run: python3 test_challenge.py")

if __name__=="__main__":main()
