# Organizer setup

Name: 04 - The Missing Minute
Category: Forensics
Type: standard
Value: 200 (suggested)
Tag: Moderate
Flag type: static, case sensitive
Flag: `TVT{a_missing_minute_left_a_trace}`
State: visible
Requirements: none
Attach ONLY: `dist/stage04-evidence.zip`

## Player description

Mira's workstation audit has a gap, but an independent monitor and collection
records survived. Reconstruct the missing minute, correlate the session and
file records, and inspect the relevant recovered object.

All evidence timestamps use UTC. Read START-HERE.txt and recovery-policy.txt
inside the attached packet. Submit the investigation receipt from the object.
This stage can be solved independently of the others.

## Optional hints

1. Compare the audit heartbeats with the independent monitor. Sort by time.
2. Join the export's session_id and file_id to the other tables.
3. The .bin extension does not identify the file format. The recovery policy
   explains both the format and the password convention.
