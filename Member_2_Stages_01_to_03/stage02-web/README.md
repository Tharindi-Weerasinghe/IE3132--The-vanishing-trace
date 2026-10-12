# Stage 02 — The Admin's Oversight

**NEW LOOPBACK-ONLY TRAINING PROTOTYPE — NOT the team's existing Flask Web-Target deployment.** The actual brief describes a Flask app at 192.168.128.30; that original app was not included in the uploads.

This Python standard-library demonstration deliberately omits an owner check on a *fictional record*. It is a toy IDOR that only binds to loopback by default and refuses arbitrary/public interfaces.

```bash
python3 test_challenge.py
python3 app.py        # starts only at http://127.0.0.1:5000
# In a second local terminal:
python3 solve.py
```

Only if your team explicitly uses the dedicated isolated lab network and has verified isolation, a Web-Target VM could bind `--host 192.168.128.30`. **Never expose this intentionally insecure sample application to the internet or a campus LAN.**

**Reset:** restart the demo server; records are static/in-memory. For the actual assignment restore Web-Target from the team's verified VM snapshot and reset CTFd scoring separately as needed.

**Still needed:** compare this prototype with the *real* Flask app, contribute the team's actual source, and test access, flag submission and reset in CTFd. The prototype cannot replace real deployment evidence.
