#!/usr/bin/env python3
"""Organizer reference solver. Uses only player evidence, never builder constants."""
import argparse
import base64
import csv
import io
from pathlib import Path
import re
from zipfile import ZipFile

def load_evidence(path):
    with ZipFile(path) as z:
        slip=z.read("dispatch-slip.txt").decode("utf-8")
        order=re.search(r"Collection order:\s*(C\d+)\s*->\s*(C\d+)",slip)
        if not order:
            raise ValueError("Dispatch order missing")
        rows=csv.DictReader(io.StringIO(z.read("catalogue.csv").decode("utf-8")))
        catalogue={row["catalogue_id"]:row["fragment"] for row in rows}
        key="".join(catalogue[record] for record in order.groups())
        compact=b"".join(z.read("message.txt").split())
        ciphertext=base64.b64decode(compact,validate=True).decode("ascii")
    return ciphertext,key

def decrypt(ciphertext,key):
    if not re.fullmatch("[A-Z]+",key):
        raise ValueError("Key must contain uppercase A-Z only")
    plain=[]
    index=0
    for char in ciphertext:
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            base=ord("A") if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" else ord("a")
            shift=ord(key[index%len(key)])-ord("A")
            plain.append(chr(base+(ord(char)-base-shift)%26))
            index+=1
        else:
            plain.append(char)
    return "".join(plain)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence",nargs="?",type=Path,
                        default=Path(__file__).resolve().parent/"dist/stage03-evidence.zip")
    args=parser.parse_args()
    ciphertext,key=load_evidence(args.evidence)
    plaintext=decrypt(ciphertext,key)
    flags=re.findall(r"TVT\{[a-z0-9_]+\}",plaintext)
    if len(flags)!=1:
        raise SystemExit("Expected one flag; review the key and cipher convention.")
    print(f"Derived keyword: {key}\n")
    print(plaintext)

if __name__=="__main__":
    main()
