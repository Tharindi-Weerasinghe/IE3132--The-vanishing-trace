# Stage 4 — The Missing Minute

Moderate digital-forensics challenge for The Vanishing Trace, following STG-04.
The player correlates an application log with independent host monitoring,
collection activity, session mappings and exported file metadata, then opens
the relevant recovered receipt. All records are synthetic and use UTC.

## Build / test / organizer solve

Kali/Ubuntu builder requirements: Python 3.8+, Info-ZIP (`zip`). Player tools:
Python 3 or unzip, file, sha256sum and a text viewer. No pip dependencies.

```bash
sudo apt install -y zip unzip
python3 build.py
python3 test_challenge.py
python3 solve.py dist/stage04-evidence.zip
```

A tested prebuilt player ZIP is included. Upload ONLY dist/stage04-evidence.zip
to CTFd. Keep this source bundle, test code and solution in the private organizer
repository. See CTFD-SETUP.md for fields, hints and the flag.

## Reset and provenance

Use a new copy of the published player ZIP and an empty extraction directory.
The builder recreates synthetic evidence, not real machine logs or a disk
image. It writes only dist/stage04-evidence.zip and dist/SHA256SUMS.txt. Encrypted
ZIP headers contain randomness, so a rebuild changes the artifact hashes;
the builder updates the metadata and checksum together. Preserve the exact
published packet. A file reset does not clear CTFd solves or scores.

The receipt password is a deliberately disclosed recovery convention derived
from the evidence; no brute-force attack is required. Legacy ZIP encryption is
used only for the fictional exercise. Test from the player download before
recording the demonstration. Difficulty remains provisional until a teammate
independently solves it and records time/hint usage.

Prepared with AI assistance. Record actual team review, build, deployment and
testing work, without attributing work to members who did not perform it.
