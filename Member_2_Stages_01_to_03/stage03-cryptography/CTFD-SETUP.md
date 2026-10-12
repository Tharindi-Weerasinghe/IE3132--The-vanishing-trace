# Organizer setup

Name: 03 - The Encrypted Message
Category: Cryptography
Type: standard
Value: 200 (suggested)
Tag: Moderate
Flag type: static, case sensitive
Flag: `TVT{the_key_was_in_the_catalogue}`
State: visible
Requirements: none
Attach ONLY: `dist/stage03-evidence.zip`

## Player description

Investigators recovered an encrypted message among Mira Sen's correspondence.
The mailroom note, cipher diary, and catalogue each explain only part of it.
Combine the evidence, recover the keyword, and decrypt Mira's message.

Everything needed is in the attached packet. You can solve this challenge
offline using a short Python script or a local cryptography tool. No previous
stage's flag is required. Submit the receipt inside the decrypted message.

## Optional hints

1. The courier wrapped the message after encryption. Undo that step first.
2. A repeating keyword and a 26-by-26 alphabet square describe Vigenere.
3. Join the catalogue fragments in dispatch order. Subtract the repeating
   keyword shifts, advancing the key only when processing a letter.
