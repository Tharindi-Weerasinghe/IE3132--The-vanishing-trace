# Stage 5 — The Silent Connection
A synthetic offline DNS/HTTP/TCP capture for The Vanishing Trace (STG-05).
24 TCP conversations include routine traffic and one collection-copy transfer.
The player identifies the request, follows its TCP stream, orders the JSON
fragments, then decodes the message. No previous stage is a prerequisite.

## Tools and commands
Kali: Python 3 + Scapy (user environment 2.7.01), Wireshark/TShark 4.6.6.
Generator/reference tests prepared with Scapy 2.7.0. No live traffic is captured
or sent. Scapy is used only to serialize packets and read/write PCAP files.

Generate the packet on Kali, then validate it:

```bash
python3 build.py
python3 test_challenge.py
```

Organizer rebuild and solution:

```bash
python3 build.py
python3 test_challenge.py
python3 solve.py dist/silent-connection.pcap
```

If a separate Python environment needs Scapy, requirements.txt records the
version used for preparation. Kali's already-installed Scapy can be used.

## Distribution and reset
Upload ONLY dist/stage05-evidence.zip, containing the PCAP and player brief.
Keep source and solution in the private organizer repository. The loose PCAP
in dist is the same one inside the player ZIP. SHA256SUMS.txt records both.
For a reset, reopen the original capture and clear display filters, or extract
a fresh player ZIP. No server state exists; this does not clear CTFd solves.
Rebuilding replaces only the three generated dist files.

## Limitations and validation
All names, addresses, contents and packet times are fictional. Documentation
address ranges and .test names are used. This is a constructed capture, not
real evidence. GUI/TShark interoperability must be verified on Kali; see
VALIDATION.md for per-environment test status. Difficulty is provisionally
Moderate-Hard; check it with an independent teammate solve.

Prepared with AI assistance; record only actual team contributions and tests.
