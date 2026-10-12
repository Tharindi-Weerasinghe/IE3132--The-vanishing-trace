# Organizer solution — Stage 3

1. Unzip the player packet and read all six files.
2. `transport-note.txt` identifies Base64. Decode `message.txt` first.
3. `cipher-diary.txt` describes Vigenere: repeated keyword, addition modulo 26
   for encryption, case preserved and the keyword advanced only on letters.
4. `dispatch-slip.txt` gives C19 then C04. In `catalogue.csv`, their fragments
   are LAN and TERN. Joining them gives LANTERN. Do not sort the IDs.
5. Decrypt by subtracting key shifts modulo 26. Copy punctuation and whitespace
   unchanged. The first letter uses L; newline characters do not reset the key.
6. Read the plaintext receipt: `TVT{the_key_was_in_the_catalogue}`.

The organizer reference solver performs this procedure using only the player
packet; it does not import the builder or read its plaintext/keyword constants.

```bash
python3 solve.py dist/stage03-evidence.zip
```

The plaintext points narratively toward the separate Missing Minute evidence.
It does not unlock that challenge or provide a prerequisite credential.

## Explanation for the demonstration

Base64 encodes bytes for transport and is reversible without a secret. Vigenere
is the encryption layer: the repeated keyword controls each alphabet shift.
The diary identifies the algorithm and exact character handling; the dispatch
and catalogue determine the key. This intentionally historical cipher is used
for the educational puzzle, not to protect real confidential information.

## Evidence to retain

Keep screenshots of decoding/keyword reconstruction, recovered plaintext,
CTFd rejection of an incorrect flag, acceptance of the correct flag, and the
scoreboard. Record another member's independent solve and any hints they needed.
