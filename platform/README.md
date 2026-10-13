# Member 1 — actual platform architecture and deployment

**Still needed:** Copy the real Docker Compose deployment (`compose.yaml`/`docker-compose.yml`, relevant non-secret nginx/site configuration and scripts) used on the CTFd-Host VM into this folder, after removing secrets. The uploaded files did **not** contain it. Please do not use a guessed Compose example as proof of a working deployment.

The briefing describes four private VMs in UTM:

| VM | Intended IP / role |
|---|---|
| Kali | 192.168.128.10 — participant |
| CTFd-Host | 192.168.128.20 — CTFd behind nginx + Redis + MariaDB |
| Web-Target | 192.168.128.30 — Stage 02 web application |
| Linux-Target | 192.168.128.40 — Stage 06 isolated target |

## Document real procedures here before grading

- VM image filenames or approved image delivery method; CPU/RAM/storage requirements.
- Exact validated setup / startup / shutdown / reset commands for your real environment.
- The actual CTFd service/container names and verified open ports.
- How the CTFd database, challenge attachments, and scoring state are preserved.
- Verified no external network adapter on any VM during the final demo.
- Actual isolation tests, flag submission validation, snapshots and recovery evidence.
- Source or configuration authored/modified by Member 1, plus commit attribution.

**Do not commit credentials, `.env`, VM disks, flags in publicly accessible files or private keys.** Keep the source repository private as long as organizer answers are present.


New review utilities in this folder:
- `inspect_platform.py`: collects read-only IP addresses, routes and running
  Docker container information **on the machine on which it is invoked**.
- `test_platform.py`: small unit tests for the route-review heuristic.
- `ARCHITECTURE.md`: architecture draft based on the uploaded briefing.
- `DEPLOYMENT-RECORD.md`: complete with genuine deploy/reset evidence.

These are AI-assisted templates/review aids and do not replace the actual
Docker Compose project or VM artifacts authored/deployed by Member 1.
