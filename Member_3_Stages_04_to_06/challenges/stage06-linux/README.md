# Stage 06 – The Final Terminal

**The Last Transmission | IE3132 Penetration Testing | Linux Security**

## Overview

*The Final Terminal* is the sixth and final challenge of **The Last Transmission**, a six-stage Capture the Flag (CTF) project. This stage focuses on Linux permissions, system security, and privilege escalation within an isolated virtual environment.

Participants examine the Linux-Target system, investigate privileged command configurations, and apply their knowledge of Linux security to complete the challenge.

## Challenge Details

| Item | Description |
|---|---|
| Stage | STG-06 |
| Challenge | The Final Terminal |
| Category | Linux Security |
| Difficulty | Hard |
| Challenge Type | Interactive, VM-based |
| Environment | Linux-Target VM |
| IP Address | 192.168.128.40 |

## Challenge Environment

The challenge operates within the project's private virtual network.

The Linux-Target VM is used specifically for this stage, allowing participants to examine system permissions and identify the intended security misconfiguration.

CTFd manages the challenge description, hints, flag submission, and scoring, while the practical task takes place within the Linux environment.

## Requirements

- Linux-Target virtual machine
- Kali Linux participant workstation
- Python 3 for the supporting verification scripts
- Access to the project's isolated virtual network

## Supporting Files

| File | Description |
|---|---|
| `check_permissions.py` | Examines saved Linux permission information |
| `test_challenge.py` | Performs local checks on the verification script |
| `fixtures/sudo-list-example.txt` | Sample permission configuration used for testing |

These scripts provide read-only verification. The Linux-Target virtual machine and its deployed challenge configuration are managed separately.

## Testing and Verification

The supporting scripts can be executed from the Stage 6 directory using:

```bash
python3 test_challenge.py
python3 check_permissions.py fixtures/sudo-list-example.txt
```

The first command checks the local verification functionality.

The second command examines a saved permission listing and checks for the relevant configuration involving the Linux `find` utility.

These checks do not modify system permissions or perform privilege escalation.

## CTFd Integration

Stage 6 is included in the CTFd platform as an interactive Linux security challenge.

Participants access the designated Linux-Target environment, investigate the configuration, and submit the recovered challenge flag through CTFd.

The challenge operates independently of the previous five stages.

## Reset and Recovery

The Linux-Target environment can be restored using the team's configured virtual machine snapshot or documented recovery procedure.

After restoration, the system configuration and participant access should be verified before the challenge is made available again.

Resetting the virtual machine does not automatically remove existing CTFd submissions or scoreboard results.

## Project Information

**Module:** IE3132 – Penetration Testing  
**Project:** The Last Transmission  
**Stage:** 06 – The Final Terminal  
**Responsible Member:** Member 3 – Challenge Design B



The project was originally named *The Vanishing Trace* and was later renamed *The Last Transmission*. The original GitHub repository URL has been retained because it was already included in the finalized assignment documentation.
