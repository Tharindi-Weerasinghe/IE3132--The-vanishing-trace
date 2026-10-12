# Organizer setup
Name: 05 - The Silent Connection
Category: Networking
Type: standard
Value: 300 (suggested)
Tag: Moderate-Hard
Flag: `TVT{the_stream_kept_the_last_word}`
Flag type: static, case sensitive
State: visible
Requirements: none
Attach ONLY: `dist/stage05-evidence.zip`

## Player description
Mira's research traffic contains a collection-copy transfer among routine
requests. Analyze the supplied capture offline, identify the relevant
conversation, reconstruct its message, and recover the transfer receipt.

Read START-HERE.txt for the workstation address and UTC time window. No live
connection or previous stage's answer is needed.

## Optional hints
1. Start with DNS and HTTP requests from the workstation during the time window.
2. Follow the TCP conversation containing the collection-copy request.
3. The application sequence numbers determine fragment order. Join the data
   fields in that order, then Base64-decode the result.
