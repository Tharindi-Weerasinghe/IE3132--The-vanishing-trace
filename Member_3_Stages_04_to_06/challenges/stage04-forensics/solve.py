#!/usr/bin/env python3
"""Organizer solver: correlates only player evidence; does not import build.py."""
import argparse
import csv
from datetime import datetime,timedelta
import hashlib
import io
from pathlib import Path
import re
from zipfile import ZipFile

def utc(s):return datetime.fromisoformat(s.replace("Z","+00:00"))
def table(z,name):return list(csv.DictReader(io.StringIO(z.read(name).decode())))

def reconstruct(path):
    with ZipFile(path) as z:
        observed={utc(line.split()[0]) for line in z.read("logs/archive-audit.log").decode().splitlines()}
        monitor=table(z,"logs/host-monitor.csv")
        expected={utc(r["timestamp_utc"]) for r in monitor}
        missing=sorted(expected-observed)
        if len(missing)!=1:raise ValueError("Expected exactly one missing heartbeat minute")
        start=missing[0];end=start+timedelta(minutes=1)
        exports=[r for r in table(z,"logs/collection-activity.csv")
                 if start<=utc(r["timestamp_utc"])<end and r["result"]=="success"]
        if len(exports)!=1:raise ValueError("Expected one successful export in the gap")
        event=exports[0]
        session=next(r for r in table(z,"logs/sessions.csv") if r["session_id"]==event["session_id"])
        if not utc(session["login_utc"])<=utc(event["timestamp_utc"])<=utc(session["logout_utc"]):
            raise ValueError("Export outside its session")
        meta=next(r for r in table(z,"filesystem-metadata.csv") if r["file_id"]==event["file_id"])
        blob=z.read(meta["recovered_path"])
        if hashlib.sha256(blob).hexdigest()!=meta["sha256"]:raise ValueError("Object hash mismatch")
        password=utc(event["timestamp_utc"]).strftime("%Y%m%d%H%M")+"_"+session["actor"]
        with ZipFile(io.BytesIO(blob)) as inner:
            note=inner.read("receipt.txt",pwd=password.encode()).decode()
        flags=re.findall(r"TVT\{[a-z0-9_]+\}",note)
        if len(flags)!=1:raise ValueError("Expected one investigation receipt")
        return {"minute":start.isoformat(),"event":event,"actor":session["actor"],
                "path":meta["recovered_path"],"password":password,"note":note,"flag":flags[0]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence",nargs="?",type=Path,default=Path(__file__).resolve().parent/"dist/stage04-evidence.zip")
    r=reconstruct(parser.parse_args().evidence)
    for key in ("minute","actor","path","password"):print(f"{key}: {r[key]}")
    print("\n"+r["note"])

if __name__=="__main__":main()
