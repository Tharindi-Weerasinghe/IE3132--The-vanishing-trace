# Stage 04 – The Missing Minute

**The Last Transmission | IE3132 Penetration Testing | Digital Forensics**

## Overview

*The Missing Minute* is the fourth challenge in **The Last Transmission**, a six-stage Capture the Flag (CTF) project. This stage focuses on digital forensics and timeline analysis.

Players investigate a collection of fictional system records to identify suspicious activity and uncover a recovered receipt containing the challenge flag.

All evidence is synthetic, and timestamps are recorded in UTC.

## Challenge Details

| Item | Description |
|---|---|
| Stage | STG-04 |
| Challenge Name | The Missing Minute |
| Category | Digital Forensics |
| Difficulty | Moderate |
| Challenge Type | File-based |

## Challenge Description

The challenge requires players to examine and correlate multiple sources of digital evidence, including application logs, host monitoring records, collection activity, session mappings, and exported file metadata.

By reconstructing the sequence of events, players must identify the relevant activity and locate the recovered receipt.

## Requirements

**Development and testing environment:**
- Kali Linux or Ubuntu
- Python 3.8 or later
- ZIP and UNZIP utilities

**Player tools:**
- Python 3 or unzip
- `file`
- `sha256sum`
- Text editor or log viewer

No additional Python packages are required.

## Build and Testing

Run the following commands from the Stage 4 directory:

```bash
sudo apt install -y zip unzip
python3 build.py
python3 test_challenge.py
python3 solve.py dist/stage04-evidence.zip
```

**File descriptions:**

- `build.py` – Generates the challenge evidence archive.
- `test_challenge.py` – Checks the generated files and challenge implementation.
- `solve.py` – Verifies the intended solution.
- `dist/stage04-evidence.zip` – Evidence archive provided to participants.
- `dist/SHA256SUMS.txt` – Checksums for the generated files.

## CTFd Configuration

The challenge is hosted through CTFd as part of The Last Transmission.

Participants download `stage04-evidence.zip` and investigate the evidence using digital forensic techniques.

Only the player evidence archive is provided through CTFd. Source files, test scripts, and solution documentation remain in the team's private repository.


## Challenge Reset

As Stage 4 is a file-based challenge, the environment can be reset by restoring the original evidence archive and extracting it into a clean directory.

The challenge files are generated from fictional data and do not contain actual system logs or disk images.

The original published ZIP should be preserved for consistency, as rebuilding an encrypted archive may produce a different checksum.

Resetting the downloaded evidence does not automatically clear participant submissions or scoreboard results in CTFd.

## Project Information

**Module:** IE3132 – Penetration Testing  
**Project:** The Last Transmission  
**Stage:** 04 – The Missing Minute  
**Responsible Member:** Member 3 – Challenge Design B



*The project was initially named The Vanishing Trace and later renamed The Last Transmission. The original GitHub repository URL has been retained because it was already included in the finalized assignment documentation.*
