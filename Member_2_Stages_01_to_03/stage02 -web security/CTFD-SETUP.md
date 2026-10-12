# Organizer setup — prototype only

Name: 02 - The Admin's Oversight
Category: Web
Type: standard
Value: 100 (suggested)
Flag type: static, case sensitive
Flag: `LTX{never_trust_the_user_id}`

Description: Mira's archived record portal lets a guest inspect their own record. Determine whether the record reference is adequately checked. Run this only in the isolated lab.

Connection: the **actual team's** Web-Target private VM address and verified service port (not a public site). This sample uses localhost by default.

Hints: (1) Study how the record URL changes. (2) Compare record IDs. (3) An application must check permissions, not just IDs.
