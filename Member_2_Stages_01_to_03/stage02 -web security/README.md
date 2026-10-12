# Stage 02 – The Admin's Oversight

## Challenge Overview

This stage focuses on web application security, specifically Insecure Direct Object Reference (IDOR) vulnerabilities. Participants investigate how missing access control checks can allow unauthorized access to application records.

## Technologies Used
- Python 3
- HTTP
- Web Application Security
- Kali Linux

## Challenge Implementation

The challenge uses a Python-based local web application to demonstrate an IDOR vulnerability. Participants analyze HTTP requests, identify insecure object references, and access a fictional record to discover the hidden flag.

This implementation is a local training prototype, separate from the team's Flask Web-Target deployment.

## How to Run

**Step 1 – Test the challenge**

```bash
python3 test_challenge.py
```

**Step 2 – Start the application**

```bash
python3 app.py
```

The application runs locally at:

`http://127.0.0.1:5000`

**Step 3 – Run the solver**

Open another terminal and execute:

```bash
python3 solve.py
```

## Testing and Validation

Testing focuses on verifying that the application starts correctly, the intended IDOR behavior can be demonstrated, and the challenge can be solved in the local environment.

## Security and Reset

The intentionally vulnerable application should only be used in an authorized, isolated testing environment.

To reset the local challenge, restart the application. For the team's deployed environment, restore the verified VM snapshot and reset CTFd scoring if necessary.

## Learning Outcome

This challenge helps participants understand IDOR vulnerabilities, insecure access controls, HTTP request analysis, and the importance of authorization checks in web applications.
