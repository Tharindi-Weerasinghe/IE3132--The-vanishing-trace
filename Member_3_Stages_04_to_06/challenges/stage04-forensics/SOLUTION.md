# Organizer solution

1. Extract stage04-evidence.zip into an empty directory. Read START-HERE.txt
   and recovery-policy.txt. Use the explicit UTC timestamps in the tables,
   never the downloaded files' local modification times.
2. Audit heartbeats skip 2026-09-29 09:16:00Z. The host monitor covers that
   minute and uptime keeps increasing. This supports an omission from the audit
   export, not a machine outage; it alone does not identify who caused it.
3. The missing window is [09:16:00Z, 09:17:00Z). Collection activity records a
   successful export at 09:16:24Z, session S41, file F071.
4. S41 maps to actor msen and spans the export time. F071 maps to recovered
   object artifacts/K7D2.bin, originally in msen's collection cache. Verify
   its size and SHA-256 against filesystem-metadata.csv.
5. `file artifacts/K7D2.bin` identifies a ZIP archive. The policy gives the
   password convention: export UTC minute + underscore + actor.
   For this event: `202609290916_msen`.
6. Run `unzip artifacts/K7D2.bin -d recovered` and enter that password.
7. Read recovered/receipt.txt and submit `TVT{a_missing_minute_left_a_trace}`.

Organizer reference solver (uses only the player packet):

```bash
python3 solve.py dist/stage04-evidence.zip
```

Useful manual commands after extracting the player ZIP:

```bash
cat logs/archive-audit.log
cat logs/host-monitor.csv
sort logs/collection-activity.csv
cat logs/sessions.csv
cat filesystem-metadata.csv
file artifacts/K7D2.bin
sha256sum artifacts/K7D2.bin
unzip artifacts/K7D2.bin -d recovered
cat recovered/receipt.txt
```

The intended task is evidence correlation, not breaking ZIP encryption.
Receipts use legacy ZIP encryption solely as a lab puzzle container. Another
route can correlate and open every object; it still requires the supplied
session and timestamp information. Do not claim the intended route is the
only possible solution or that the container provides modern secure storage.

Evidence: missing minute comparison, export/session/file correlation, hash
check, recovered receipt, incorrect/correct CTFd submissions, independent solve.
