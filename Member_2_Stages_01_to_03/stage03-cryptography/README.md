# Stage 3 — The Encrypted Message

The Vanishing Trace: moderate cryptography puzzle following proposal STG-03.
Players combine separate clues to identify a Base64 wrapper, Vigenere cipher,
and a keyword assembled in dispatch order from catalogue fragments.

## Requirements

Python 3.8 or later; standard library only. Works offline on Kali, Ubuntu,
and Windows with Python installed. No additional packages or services.

## Build, test, and solve (organizer)

```bash
python3 build.py
python3 test_challenge.py
python3 solve.py dist/stage03-evidence.zip
```

On Windows, use `py -3` if that is your Python launcher. A ready-built player
packet is included in `dist/`. The builder writes only its two generated files
there. Fixed ZIP timestamps make the player packet reproducible in the same
Python/zlib environment; compressed bytes may vary across library versions.

## Distribution

Upload ONLY `dist/stage03-evidence.zip` to CTFd. The outer source bundle contains
answers, the builder and the reference solver; keep it in the private organizer
repository. `dist/SHA256SUMS.txt` records the exact player packet's hash.
Use `CTFD-SETUP.md` for the description, flag, score and optional hints.

## Reset

Static evidence has no server state. Start from a fresh downloaded player ZIP
and an empty working directory. Rebuild from source if needed. Resetting files
does not clear CTFd submissions or scores. Preserve the published ZIP and hash.

## Validation and difficulty

See VALIDATION.md for actual preparation tests and remaining user-side checks.
Difficulty is provisionally Moderate; a teammate must independently solve it
and record elapsed time/hints before finalizing difficulty. The intended route
requires combining clues rather than blind cryptanalysis. No earlier stage is
a prerequisite.

## Credits

Prepared with AI assistance for the university project. Team members should
record only their actual review, implementation, deployment and testing work.
