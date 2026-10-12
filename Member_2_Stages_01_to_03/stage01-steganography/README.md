# Stage 01 — The Photographer's Secret

**NEW REFERENCE STARTER — not recovered original team source.**

This recreates the learning objective described in the briefing: inspect JPEG metadata for a phrase, use **steghide** on the image, and recover a fictional receipt. The image is generated locally; it is not Mira's original photo. The builder uses Pillow and the Kali `steghide` utility.

On **your isolated Kali VM**, install Pillow if needed and ensure `steghide` is already available. Run:

```bash
python3 build.py
python3 test_challenge.py
python3 solve.py dist/stage01-evidence.zip
```

The builder intentionally fails if `steghide` is absent. Tests are only meaningful if they run on the published packet. Attach **only** `dist/stage01-evidence.zip` to CTFd. Never attach this source or `SOLUTION.md` to player-facing challenge files.

**Reset:** extract the original published player ZIP again; on the platform reset scoring separately if required. Replace this starter with the team's actual created Stage 01 if it differs from what you demonstrated.
