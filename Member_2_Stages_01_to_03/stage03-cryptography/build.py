#!/usr/bin/env python3
"""Organizer-only reproducible Stage 3 fixture builder; Python standard library."""
import base64
import csv
import hashlib
import io
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
KEY = "LANTERN"
FLAG = "TVT{the_key_was_in_the_catalogue}"
PLAINTEXT = """MIRA SEN / PRIVATE CORRESPONDENCE
2026-09-29 09:05 UTC

The archive entry was only one part of my record. Someone removed a minute
from the collection history. Compare independent records before trusting a
single clock. The evidence for that question is in a separate case packet.

Encrypted-message receipt: TVT{the_key_was_in_the_catalogue}

Mira
"""

def encrypt(text, key):
    shifts = [ord(c) - 65 for c in key]
    result = []
    cursor = 0
    for char in text:
        if "A" <= char <= "Z" or "a" <= char <= "z":
            start = 65 if char.isupper() else 97
            result.append(chr(start + (ord(char)-start + shifts[cursor % len(shifts)]) % 26))
            cursor += 1
        else:
            result.append(char)
    return "".join(result)

def player_files():
    cipher = encrypt(PLAINTEXT, KEY).encode("ascii")
    wrapped = base64.b64encode(cipher).decode("ascii")
    wrapped = "\n".join(wrapped[i:i+76] for i in range(0,len(wrapped),76)) + "\n"
    rows = [
        ("C27", "FIELD", "field ledger"),
        ("C04", "TERN", "bird survey card"),
        ("C31", "RAIN", "weather observations"),
        ("C12", "MOSS", "specimen register"),
        ("C19", "LAN", "storage shelf label"),
        ("C08", "DUSK", "lighting survey"),
    ]
    table = io.StringIO(newline="")
    writer=csv.writer(table,lineterminator="\n")
    writer.writerow(("catalogue_id","fragment","description"))
    writer.writerows(rows)
    return {
        "START-HERE.txt": """THE VANISHING TRACE / CASE PACKET 03
Recovered: 2026-09-29 09:10 UTC

This packet contains a wrapped encrypted message and three pieces of context.
Work out how it was wrapped, which letter transformation Mira used, and how
she assembled its keyword. Decrypt the note and submit its receipt.

All required evidence is in this packet. No account, internet service, or
answer from another challenge is required. Preserve punctuation and case.
""",
        "message.txt": wrapped,
        "transport-note.txt": """COPY OF A MAILROOM NOTE
Our text courier allows the 64-symbol alphabet A-Z, a-z, 0-9, + and /.
An equals sign is padding. Line breaks were inserted only for readability.
The courier wrapper was applied LAST, after Mira's letter transformation.
Remove that wrapper first; it is an encoding, not her encryption.
""",
        "cipher-diary.txt": """MIRA'S CIPHER DIARY / 2026-09-28
A single Caesar shift was too predictable. I switched to the old 26-by-26
alphabet square and a repeating keyword: a different row for each letter.

My convention: A is 0, B is 1, ... Z is 25. To encrypt, ADD the current
keyword letter's value to the message letter's value, wrapping at 26.
The keyword starts again when exhausted. Advance it only for ASCII letters
A-Z or a-z. Preserve letter case. Copy digits, spaces, punctuation, underscores
and line breaks unchanged; they do not consume keyword letters.

The dispatch slip identifies my keyword fragments. Keep its written order.
""",
        "dispatch-slip.txt": """INTERNAL DISPATCH / 2026-09-29 08:55 UTC
Collection order: C19 -> C04

The catalogue's FRAGMENT cells hold the pieces of my keyword.
Join just those two cells in dispatch order, with no separator.
The other catalogue entries belong to unrelated collections.
""",
        "catalogue.csv": table.getvalue(),
    }

def main():
    out=ROOT/"dist"
    out.mkdir(exist_ok=True)
    target=out/"stage03-evidence.zip"
    with ZipFile(target,"w",compression=ZIP_DEFLATED) as z:
        for name,text in sorted(player_files().items()):
            info=ZipInfo(name, date_time=(2026,9,29,9,10,0))
            info.compress_type=ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,text.encode("utf-8"))
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    (out/"SHA256SUMS.txt").write_text(f"{digest}  stage03-evidence.zip\n",encoding="utf-8")
    print(f"PLAYER FILE: {target}")
    print(f"SHA256: {digest}")
    print("Next run: python3 test_challenge.py")

if __name__=="__main__":
    main()
