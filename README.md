# The Last Transmission

**IE3132 – Penetration Testing | Assignment 02**

The Last Transmission is a six-stage Capture the Flag (CTF) project developed for IE3132 Penetration Testing. The project follows a fictional investigation involving Mira Sen, where participants solve a series of challenges using different cybersecurity techniques.

The challenges are hosted on CTFd within an isolated virtual lab, allowing participants to investigate digital evidence, identify vulnerabilities, and submit flags to complete each stage.

## Project Name

The project was initially named **The Vanishing Trace** and was later renamed **The Last Transmission**. We have retained the original GitHub repository name because its link was already included in our finalized assignment documentation. Both names refer to the same project.

## Challenges

| Stage | Challenge | Category |
|---|---|---|
| 01 | The Photographer's Secret | Steganography |
| 02 | The Admin's Oversight | Web Security (IDOR) |
| 03 | The Encrypted Message | Cryptography |
| 04 | The Missing Minute | Digital Forensics |
| 05 | The Silent Connection | Network Analysis (PCAP) |
| 06 | The Final Terminal | Linux Security |

Each stage focuses on a different security concept. The challenges include downloadable evidence files, web-based tasks, network traffic analysis, and a Linux-based practical exercise.

## System Architecture

The project uses CTFd as the main platform for managing challenges, validating flags, displaying hints, and maintaining the scoreboard.

The virtual lab consists of four machines connected through a private network.

| Virtual Machine | IP Address | Purpose |
|---|---|---|
| Kali Linux | 192.168.128.10 | Participant workstation |
| CTFd-Host | 192.168.128.20 | CTF platform and scoreboard |
| Web-Target | 192.168.128.30 | Web security challenge |
| Linux-Target | 192.168.128.40 | Linux security challenge |

CTFd is deployed using Docker Compose with nginx, CTFd, MariaDB, and Redis.

## Repository Structure

- **challenges/** – Source files, build scripts, solver scripts, test files, and documentation for all six stages.
- **platform/** – Platform configuration, architecture information, and environment checks.
- **testing/** – Integration testing, validation scripts, and test documentation.
- **docs/** – Additional project documentation and supporting files.
- **README.md** – Main project overview and instructions.

The `challenges` directory is organized into six folders: `stage01-stego`, `stage02-web`, `stage03-crypto`, `stage04-forensics`, `stage05-network`, and `stage06-linux`.

## Setup and Execution

1. Start the four virtual machines and connect them to the configured private network.
2. On the CTFd-Host, navigate to the Docker Compose deployment directory.
3. Run `docker compose up -d` to start the CTFd services.
4. Run `docker compose ps` to check the running containers.
5. Open `http://192.168.128.20` from the Kali Linux browser.
6. Log in to CTFd and access the challenges.

Stage-specific instructions and supporting scripts are provided in the relevant challenge folders.

### Challenge Reset

For static challenges (Stages 1, 3, 4, and 5), restore the original challenge files from the saved copies.

For interactive challenges (Stages 2 and 6), restore the respective target environment using the configured VM snapshots or reset procedures.

## Team Contributions

| Member | Responsibilities |
|---|---|
| Member 1 | CTF Platform and Architecture |
| Member 2 | Challenge Design and Implementation – Stages 1–3 |
| Member 3 | Challenge Design and Implementation – Stages 4–6 |
| Member 4 | Integration, Testing, Validation, and Documentation |



---

*IE3132 Penetration Testing – Group Assignment 02*
