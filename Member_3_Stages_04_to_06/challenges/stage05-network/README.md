# Stage 05 – The Silent Connection

**The Last Transmission | IE3132 Penetration Testing | Network Analysis**

## Overview

*The Silent Connection* is the fifth stage of **The Last Transmission**, a six-stage Capture the Flag (CTF) project. This challenge focuses on network traffic analysis using a synthetic packet capture (PCAP).

The capture contains **24 TCP conversations**, including everyday network activity and a single collection-copy transfer. Participants identify the relevant HTTP request, follow its TCP stream, arrange the JSON fragments in the correct order, and decode the recovered message to obtain the flag.

This stage can be completed independently; no flags or results from earlier stages are required.

## Challenge Details

| Item | Description |
|---|---|
| Stage | STG-05 |
| Challenge | The Silent Connection |
| Category | Network Analysis (PCAP) |
| Difficulty | Moderate–Hard (subject to independent playtesting) |
| Challenge type | Offline, file-based |

## Requirements

- Kali Linux or another compatible Linux environment
- Python 3
- Scapy for generating and validating the PCAP
- Wireshark or TShark for packet analysis

The capture was prepared using **Scapy 2.7.0**. The documented Kali environment uses **Wireshark/TShark 4.6.6** and a reported Scapy version of **2.7.01**. The `requirements.txt` file records the preparation dependency for environments that need it installed separately.

The traffic is generated locally. The scripts do not capture or transmit live network traffic.

## Build and Testing

From the `stage05-network` directory, run:

```bash
python3 build.py
python3 test_challenge.py
```

To verify the intended solution using the generated PCAP:

```bash
python3 solve.py dist/silent-connection.pcap
```

### Main Files

| File | Purpose |
|---|---|
| `build.py` | Generates the synthetic capture and player ZIP |
| `test_challenge.py` | Performs automated checks on the generated files |
| `solve.py` | Verifies the intended solution from the capture |
| `requirements.txt` | Records the Scapy preparation dependency |
| `dist/silent-connection.pcap` | Generated packet capture |
| `dist/stage05-evidence.zip` | Player download containing the PCAP and challenge brief |
| `dist/SHA256SUMS.txt` | Checksums of the generated distribution files |
| `VALIDATION.md` | Records testing and compatibility checks |

## CTFd Distribution

Only **`dist/stage05-evidence.zip`** should be attached to the participant-facing challenge in CTFd. It contains the PCAP and player instructions.

Keep `build.py`, `solve.py`, testing files, and organizer solutions in the team's **private** source repository. The standalone PCAP in `dist/` is the same file included in the player ZIP, and the checksum file records both artifacts.

## Reset Procedure

As Stage 5 is an offline challenge, no separate target server needs to be reset. To start again, reopen the original PCAP and clear Wireshark display filters, or extract a fresh copy of the published player ZIP.

This reset does **not** remove participant solves or change scores in CTFd. Running the builder again replaces the three generated files in `dist/`, so retain the exact version published to players.

## Validation Notes

All packet contents, names, addresses, and timestamps are fictional. The capture uses documentation IP ranges and `.test` domain names; it is not evidence collected from a real network.

Automated checks are provided in `test_challenge.py`. Wireshark/TShark compatibility and the final difficulty assessment should be confirmed in the actual Kali environment and through an independent teammate solve. See `VALIDATION.md` for the recorded status of those checks.

## Project Information

**Module:** IE3132 – Penetration Testing  
**Project:** The Last Transmission  
**Stage:** 05 – The Silent Connection  
**Responsible team role:** Member 3 – Challenge Design B  
**Repository:** [The Last Transmission](https://github.com/Tharindi-Weerasinghe/IE3132--The-vanishing-trace)

The project was previously called *The Vanishing Trace*. Its GitHub URL retains the original name because it was referenced in finalized assignment documentation.

