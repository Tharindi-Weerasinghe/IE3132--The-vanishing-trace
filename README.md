# The Last Transmission

**IE3132 Penetration Testing | Assignment 02 | Six-stage CTFd lab**

> **Repository naming note:** The project was originally named **The Vanishing Trace** and the existing GitHub repository URL contains that name. The team subsequently adopted **The Last Transmission** as the final project title. We are keeping the original GitHub repository URL because it was already included in submitted/finalized documentation. The repository name and some older `TVT` file identifiers are therefore historical; the official project title is **The Last Transmission**. GitHub permits repository renames, but we are deliberately leaving this URL unchanged to preserve existing references.
>
> **Important:** This ZIP is an integration draft, **not yet a complete, deployment-verified submission**. Uploaded Stage 03–05 files have been retained; Stage 01/02/06 contain new reference starters, not recovered originals. Verify and replace them with the team's genuine deployed work. Read [docs/ALIGNMENT_REPORT.md](docs/ALIGNMENT_REPORT.md) before marking the project final.

## Project at a glance

The fictional investigator follows Mira Sen's traces across six independent challenges. The actual IE3132 briefing describes an **isolated four-VM lab** with CTFd (nginx, CTFd app, MariaDB, Redis), a participant Kali VM, a web target, and a Linux target. This archive does **not** include those VM images or the team's original deployment configuration.

| Stage | Domain / challenge | Responsibility | Content status |
|---|---|---|---|
| 01 | The Photographer's Secret — steganography | Member 2 | **New prototype builder/solver; requires steghide on Kali and validation** |
| 02 | The Admin's Oversight — web/IDOR | Member 2 | **New loopback-only demonstration app; replace/compare with real Flask Web-Target** |
| 03 | The Encrypted Message — cryptography | Member 2 | **Provided source bundle; 8 local tests passed** |
| 04 | The Missing Minute — forensics | Member 3 | **Provided source bundle; 8 local tests passed** |
| 05 | The Silent Connection — network/PCAP | Member 3 | **Provided source bundle; Scapy runtime tests not run here** |
| 06 | The Final Terminal — Linux security | Member 3 | **Read-only verification starter; actual target VM and setup/solver still required** |

**Members 1 and 4:** `platform/` contains read-only environment review tools and deployment evidence templates, not the real Docker Compose project; `testing/` contains unit-test runners, structural checks and templates. All newly generated helpers require review and honest attribution. Actual VM snapshots, Docker Compose configuration, results and evidence must come from team members themselves.

## Files and roles

```text
challenges/
  stage01-stego/         new reference builder, player packet, solver, tests
  stage02-web/           new localhost-only prototype, solver, tests
  stage03-crypto/        provided original ZIP contents
  stage04-forensics/     provided original ZIP contents
  stage05-network/       provided original ZIP contents
  stage06-linux/         read-only validation starter; no VM image
platform/                Member 1: configuration and architecture evidence
 testing/                Member 4: review tooling and real test-result templates
 docs/                   name note, reconciliation, contribution checklist
```

## Organizer setup / run / reset

1. **Keep this repository private** while it contains `SOLUTION.md`, `CTFD-SETUP.md`, answer strings, sample credentials, or private testing materials. These are *organizer files*, not player downloads.
2. On the isolated lab, **Member 1** must provide the real VM image(s) or the actual Docker Compose project and accurate start/stop/reset steps in `platform/README.md`. Do not treat the example Compose placeholder as deployable.
3. **Members 2–3** should build and validate the stages **inside their intended environments** and attach only the specified player files in CTFd. See each stage's README and CTFD-SETUP.md.
4. **Member 4** checks all six stages as a player, records wrong/correct flag submission, verifies reset/isolation, and fills the testing matrix honestly. Run `python3 testing/check_repository.py` to list missing files and flag-format inconsistencies.
5. Preserve the actual generated artifact attached to CTFd and its checksum. A rebuild may change bytes; do not assume a newly built file matches an earlier published attachment.
6. Static stages (01,03,04,05): reset by extracting a fresh copy of the original published player packet. Live stages (02,06): restore the actual target VM/container to its known-good snapshot **using the team's tested procedures**. Neither reset clears CTFd solves/scoreboard automatically.

### Stage-specific commands (from each stage directory)

| Stage | Preparation / tests | Dependencies |
|---|---|---|
| 01 | `python3 build.py && python3 test_challenge.py` | Python, Pillow, **steghide** |
| 02 | `python3 test_challenge.py`; `python3 app.py` | Python standard library; **prototype on localhost** |
| 03 | `python3 build.py && python3 test_challenge.py` | Python standard library |
| 04 | `python3 build.py && python3 test_challenge.py` | Python, Info-ZIP `zip` and `unzip` |
| 05 | `python3 build.py && python3 test_challenge.py` | Python + Scapy (Kali), optional TShark |
| 06 | `python3 test_challenge.py` | Python; only checks saved sample policy text |

**Flag mismatch requiring team decision:** the briefing specifies `LTX{...}` for all stages, but the **supplied source** for 03–05 uses `TVT{...}`. The starter for 01–02 uses `LTX{...}`. Do not claim consistency or silently change flags; first agree on the authoritative convention, rebuild affected challenge packets, revise solutions, and update all six CTFd flag fields before re-testing.

**Design mismatch requiring team decision:** the supplied Stage 03 uses Base64 + Vigenere, Stage 04 synthetic multi-log reconstruction, and Stage 05 a fragment-ordered HTTP transfer. These differ from some steps of the briefing/video game plan. Treat the real deployed build as authoritative and update documentation/video plans after verifying it, not vice versa.

## Credits and honesty

- Source for Stages 03, 04, 05 comes unchanged from the team's uploaded ZIP files, some of which explicitly credit AI assistance.
- New Stage 01, Stage 02 and Stage 06 starter content, root README, and review scripts were drafted with AI assistance and **must not be presented as already implemented or personally written by the named team members**. Review, edit, test and attribute contributions accurately.
- Do not read AI-generated narration in the demonstration: the uploaded game plan says the graded demonstration must be live and unscripted in each member's own words.
- Record actual testing evidence and named Git commit history. Do not invent screenshots, results, or authorship.

See [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md) and [docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md).
