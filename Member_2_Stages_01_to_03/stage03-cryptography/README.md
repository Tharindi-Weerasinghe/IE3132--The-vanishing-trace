# Stage 03 – The Encrypted Message

## Challenge Overview

This stage focuses on cryptography and encrypted message analysis. Participants must investigate hidden clues, identify encryption techniques, and decrypt a secret message to recover the CTF flag.

## Technologies Used
- Python 3
- Base64 Encoding
- Vigenère Cipher
- Cryptography Techniques
- Kali Linux

## Challenge Implementation

The challenge combines Base64 encoding and Vigenère encryption to protect a secret message. Participants collect clues from different files, identify the correct keyword, and apply decryption techniques to reveal the hidden flag.

## How to Run

**Step 1 – Build the challenge**

```bash
python3 build.py
```

**Step 2 – Test the challenge**

```bash
python3 test_challenge.py
```

**Step 3 – Run the solver**

```bash
python3 solve.py dist/stage03-evidence.zip
```

## Testing and Validation

Testing focuses on verifying that the challenge files are generated correctly, the encrypted message can be decoded, and the expected CTF flag can be recovered.

The challenge is designed for a moderate difficulty level. Independent testing is recommended before final deployment.

## Deployment

Upload only `dist/stage03-evidence.zip` to the CTFd platform.

Keep the source code, solution scripts, and organizer documentation private to prevent revealing the challenge answers.

## Security and Reset

The challenge uses static files and does not require an active server.

To reset the challenge, extract a fresh copy of the player ZIP into an empty working directory. Reset CTFd submissions and scores separately if required.

## Learning Outcome

This challenge helps participants develop practical skills in cryptography, Base64 decoding, Vigenère cipher analysis, logical problem-solving, and extracting information from encrypted messages.
