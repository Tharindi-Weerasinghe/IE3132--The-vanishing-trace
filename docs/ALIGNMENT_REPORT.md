# Integration audit and decisions still required

**Scope:** based on the team's 46-page briefing pack and Assignment 02 game plan, plus the three supplied source ZIP files; no CTFd server or real VM was accessible to the package author.

## Critical conflicts — require team confirmation before final upload

1. **Naming:** Official title is *The Last Transmission*. Original repo slug is *IE3132--The-vanishing-trace*. Keep original URL to preserve the link in finalized documentation; acknowledge historical naming. Names inside supplied stage files are also historical.
2. **Flags:** Briefing and game plan specify `LTX{...}`. Supplied Stages 03–05 use `TVT{...}` within code, docs and/or player artifacts. The builder/test suites depend on those exact values. Changing only one text file will break consistency; coordinate a deliberate project-wide update with the real CTFd admin if required.
3. **Stage 03 mechanism:** Game plan mentions Base64 + ROT13; supplied files implement Base64 + **Vigenere** with a catalogue key. These are not interchangeable.
4. **Stage 04 story/evidence:** Game plan uses `auth.log`, `access.log`, `process_list.txt` and a 02:16–02:17 timeline. Uploaded packet uses an independent monitor, collection/session CSV tables and a **09:16 UTC** missing minute. Match recorded demonstration to deployed evidence.
5. **Stage 05 PCAP:** Game plan mentions a token in an HTTP header; supplied Stage 05 builds a **synthetic PCAP with JSON application fragments requiring Base64 reconstruction**. Ensure the demo and scoring match the actual deployed challenge.
6. **Missing original source:** We received no Stage 01/02/06 source or VM snapshot from the actual team. Files created for those folders in this package are explicitly new reference starters, not evidence of previous implementation. Stage 06 does not provision any privileged VM.
7. **No real deployment package:** The actual Member 1 Docker Compose project, private network settings, VM images and recovery commands were not supplied. An organizer must collect them before claiming this package is fully deployable.
8. **Member 4 evidence:** Real test logs, cross-testing reports, risk register decisions and commit history must be collected; templates do not substitute for tests.

## Checks carried out on these provided files

- Stage 03 original files: syntax checked, **8/8 tests passed** locally.
- Stage 04 original files: syntax checked, **8/8 tests passed** locally.
- Stage 05 original files: syntax checked. Runtime tests **not run**: Scapy was not available in the evaluation environment; it also needs TShark/manual player confirmation.
- New Stage 01 and Stage 06 code: local/static checks only unless documented later.
- New Stage 02: standalone Python proof-of-concept test only, not the deployed Flask system.
- Nothing was tested against the team's CTFd UI or private VM network.

## Player artifact versus organizer source

Never upload `build.py`, `solve.py`, `CTFD-SETUP.md` or `SOLUTION.md` as a participant-facing CTFd attachment. Players receive only player packets from `dist/` (or the specific deployed web/Linux target). Keep organizer answer keys and actual student testing logs in a restricted repository.
