# Member 4 – Testing and Documentation

## The Vanishing Trace | IE3132 – Penetration Testing

### Overview

This folder contains the testing scripts and documentation used to support the verification and evaluation of *The Vanishing Trace* CTF project.

### Main Responsibilities

- **Functional Testing:** Check the functionality of all six CTF challenges.
- **Flag Validation:** Verify correct and incorrect flag submissions.
- **Integration Testing:** Check challenge integration with the CTFd platform.
- **Security Testing:** Review network isolation and identify potential security issues.
- **Recovery Testing:** Verify challenge reset and system restoration procedures.
- **Documentation:** Record testing results, identified defects, and design changes.

### Testing Scripts

**1. Repository Checker**

Checks the project folder structure and identifies possible flag-format issues.

```bash
python3 testing/check_repository.py
```

**2. Stage Test Runner**

Runs available local test suites for the six challenges and reports their results.

```bash
python3 testing/run_stage_tests.py
```

### Testing Documentation

- `TEST_MATRIX.csv` – Records test cases and results.
- `RISK_REGISTER_TEMPLATE.csv` – Documents identified risks and mitigation measures.
- `CHANGE_LOG_TEMPLATE.md` – Records project modifications and improvements.

### Testing and Validation

The testing process covers challenge functionality, flag validation, system integration, and recovery procedures.

Local script results are recorded separately from live CTFd testing. Platform validation, network isolation, and recovery tests require verification in the deployed environment.

### Summary

Member 4's work focuses on supporting the quality, security, and reliability of the CTF project through testing scripts, verification procedures, and structured documentation.
