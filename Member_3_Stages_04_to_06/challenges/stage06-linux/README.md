# Stage 06 — The Final Terminal

**INCOMPLETE REFERENCE STARTER.** This directory does **not** provision a Linux privilege-escalation VM, install sudo rules, provide a working server, or reproduce the team's final challenge. The briefing says Stage 06 is a **live isolated Linux-Target VM** at 192.168.128.40, and a VM snapshot is needed for a complete submission. No VM image or actual provisioning/solver scripts were uploaded here.

The only code in this directory is a **read-only** helper that examines saved `sudo -l` text and checks if a potentially problematic rule involving `find` is present. It makes no connection to any host and performs no escalation.

```bash
python3 test_challenge.py
python3 check_permissions.py fixtures/sudo-list-example.txt
```

Before submitting, Member 3 should contribute the genuinely developed Linux-Target setup/configuration and lab-specific solver, along with the verified VM snapshot, access controls, player instructions, reset/recovery procedure, CTFd validation, and evidence. This scaffold alone **cannot count as a working sixth stage**.

Do not publish any live private credentials or actual VM secrets. Run tests only on your team's isolated and authorized lab.
