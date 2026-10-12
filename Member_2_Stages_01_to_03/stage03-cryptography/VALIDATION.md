# Preparation validation

The eight tests in `test_challenge.py` passed in the preparation environment:
standard Vigenere test vector; key reconstructed from player files; exact
plaintext and single flag; seven plausible wrong keys produce no flag; case
and punctuation handling; allowlisted player files without exposed plaintext
flag or joined keyword; standalone offline solver; SHA-256 manifest.

A second build produced a byte-identical player ZIP in this environment.

Remaining: run tests on Kali, upload to CTFd, solve the downloaded copy as a
normal player, verify incorrect/correct submissions and 200-point scoring,
and have another group member independently solve and assess the difficulty.
These remaining tests are not claimed to have passed.
