#!/usr/bin/env python3
"""Organizer-only fictional forensic fixture generator."""
import csv
from datetime import datetime, timezone
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parent
FLAG="TVT{a_missing_minute_left_a_trace}"
# Timestamp, file ID, session ID, actor, original basename. Deliberately unsorted.
EXPORTS=[
 ("2026-09-29T09:18:11Z","F082","S52","cataloguer","P2A8.bin"),
 ("2026-09-29T09:14:37Z","F063","S39","assistant","B9F1.bin"),
 ("2026-09-29T09:16:24Z","F071","S41","msen","K7D2.bin"),
 ("2026-09-29T09:12:18Z","F051","S30","cataloguer","R4M6.bin"),
 ("2026-09-29T09:20:44Z","F095","S60","assistant","V3C5.bin"),
]
SESSIONS=[
 ("S52","cataloguer","2026-09-29T09:17:30Z","2026-09-29T09:19:00Z"),
 ("S39","assistant","2026-09-29T09:14:00Z","2026-09-29T09:15:10Z"),
 ("S60","assistant","2026-09-29T09:20:00Z","2026-09-29T09:21:00Z"),
 ("S41","msen","2026-09-29T09:15:55Z","2026-09-29T09:17:02Z"),
 ("S30","cataloguer","2026-09-29T09:12:00Z","2026-09-29T09:13:00Z"),
]

def csv_bytes(fields,rows):
    s=io.StringIO(newline="")
    w=csv.writer(s,lineterminator="\n");w.writerow(fields);w.writerows(rows)
    return s.getvalue().encode()

def minute_key(timestamp,actor):
    return datetime.fromisoformat(timestamp.replace("Z","+00:00")).strftime("%Y%m%d%H%M")+"_"+actor

def main():
    if not shutil.which("zip"):
        raise SystemExit("Builder needs Info-ZIP: sudo apt install zip")
    evidence={}
    evidence["START-HERE.txt"]=b"""THE VANISHING TRACE / CASE PACKET 04 / THE MISSING MINUTE
All event times are UTC (Z). Everything here is fictional lab evidence.

The archive audit claims to cover 09:12:00 through 09:20:59 on 2026-09-29.
It should contain one heartbeat at second 00 of every minute in that interval.
An independent host monitor and collection subsystem were also recovered.
Find the absent minute, establish what the collection subsystem did then,
identify the recovered object, and inspect its receipt.

The CSV tables were recovered out of order. Correlate IDs, not row positions.
No previous challenge's flag is required. Do not execute recovered objects.
Use recovery-policy.txt to interpret the evidence and open collection receipts.
"""
    evidence["recovery-policy.txt"]=b"""RECOVERY NOTES / FORMAT GUIDE
All CSV timestamp fields and audit-log timestamps are UTC. Do not convert them
to local time. Filesystem timestamps on this downloaded ZIP or its extracted
files describe packaging/extraction, not the original activity; use the CSVs.

logs/archive-audit.log: application heartbeat every minute; this is the
  questioned export of the application audit, not an independent system clock.
logs/host-monitor.csv: independent host liveness samples.
logs/collection-activity.csv: separate collection subsystem, timestamped after
  a collection export completed; its file_id joins to filesystem-metadata.csv.
logs/sessions.csv: session-to-actor mapping and session boundaries.
filesystem-metadata.csv: original file metadata plus the path and SHA-256 of
  each recovered object's bytes. This is synthetic exported metadata, not an
  actual disk image. All original mtimes equal creation times in this fixture.

Collection objects use ZIP format despite their .bin extension. The standard
receipt recovery password is the export completion minute in UTC, formatted
YYYYMMDDHHMM, followed by an underscore and the session's actor exactly as
written. Use the session referenced by the export, not a nearby login.

Example for an unrelated case: 2026-01-02T03:04:59Z, actor visitor
becomes 202601020304_visitor. Seconds are discarded, not rounded.

List an object with file/unzip, verify its SHA-256, then open its receipt with
unzip. Reconstruct the absent minute and identify the relevant export first.
"""
    minutes=list(range(12,21))
    evidence["logs/archive-audit.log"]="".join(
        f"2026-09-29T09:{m:02d}:00Z service=archive event=heartbeat status=ok\n"
        for m in minutes if m!=16).encode()
    evidence["logs/host-monitor.csv"]=csv_bytes(
        ["timestamp_utc","host","state","uptime_seconds"],
        [(f"2026-09-29T09:{m:02d}:00Z","mira-workstation","up",7200+(m-12)*60) for m in minutes])
    evidence["logs/sessions.csv"]=csv_bytes(
        ["session_id","actor","login_utc","logout_utc"],SESSIONS)
    evidence["logs/collection-activity.csv"]=csv_bytes(
        ["timestamp_utc","session_id","operation","file_id","result"],
        [(t,s,"collection_export",fid,"success") for t,fid,s,a,n in EXPORTS])
    metadata=[]
    with tempfile.TemporaryDirectory(prefix="tvt-stage04-") as temp:
        work=Path(temp)
        for t,fid,s,actor,name in EXPORTS:
            message=(f"COLLECTION RECEIPT\nUTC: {t}\nActor: {actor}\nFile ID: {fid}\n\n")
            if fid=="F071":
                message+=("I saved the collection history while the workstation was still online.\n"
                          "This copy survived outside the application's shortened audit export.\n"
                          "The separate connection capture may explain what happened later.\n\n"
                          f"Investigation receipt: {FLAG}\n")
            else:
                message+="Routine collection export. This receipt is outside the missing interval.\n"
            receipt=work/"receipt.txt";receipt.write_text(message,encoding="utf-8")
            epoch=datetime.fromisoformat(t.replace("Z","+00:00")).timestamp()
            os.utime(receipt,(epoch,epoch))
            archive=work/(name+".zip")
            subprocess.run(["zip","-q","-X","-P",minute_key(t,actor),str(archive),"receipt.txt"],
                           cwd=work,env={**os.environ,"TZ":"UTC"},check=True,capture_output=True)
            data=archive.read_bytes()
            recovered="artifacts/"+name
            evidence[recovered]=data
            metadata.append((fid,f"/home/{actor}/.cache/collection/{name}",t,t,len(data),
                             hashlib.sha256(data).hexdigest(),recovered))
    evidence["filesystem-metadata.csv"]=csv_bytes(
        ["file_id","original_path","created_utc","modified_utc","size_bytes","sha256","recovered_path"],metadata)
    out=ROOT/"dist";out.mkdir(exist_ok=True)
    target=out/"stage04-evidence.zip"
    with ZipFile(target,"w",compression=ZIP_DEFLATED) as z:
        for name,data in sorted(evidence.items()):
            info=ZipInfo(name,(2026,9,29,10,0,0));info.compress_type=ZIP_DEFLATED
            info.external_attr=0o100644<<16;z.writestr(info,data)
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    (out/"SHA256SUMS.txt").write_text(f"{digest}  stage04-evidence.zip\n")
    print(f"PLAYER FILE: {target}\nSHA256: {digest}\nNext run: python3 test_challenge.py")

if __name__=="__main__":main()
