# Proposed platform architecture (from the team briefing, not independently observed)

| VM | Planned address | Purpose |
|---|---|---|
| Kali | 192.168.128.10 | Participant browser and tools |
| CTFd-Host | 192.168.128.20 | nginx, CTFd, MariaDB, Redis via Docker Compose |
| Web-Target | 192.168.128.30 | Stage 02 interactive application |
| Linux-Target | 192.168.128.40 | Stage 06 isolated Linux target |

The briefing requires an isolated `192.168.128.0/24` private lab. A previous draft
mentions a temporary Shared network adapter. Verify that **all** unwanted
adapters have been removed using real VM network settings, and record actual
isolation evidence. The `inspect_platform.py` helper collects local Linux
information but does **not** establish the hypervisor's isolation state.

**Deployment not included:** No Compose YAML, VM image, credentials or live
validation logs were provided. Member 1 must attach *real* files and evidence.
