# Organizer solution

1. Download and extract stage05-evidence.zip. Read START-HERE.txt.
2. Open silent-connection.pcap in Wireshark (File > Open, not live capture).
   Set time display to UTC Date and Time if inspecting clock values.
3. Review `dns` and `http.request`. Mira's source is 192.0.2.10. The relevant
   window is 2026-09-29 09:17:30–09:17:40 UTC.
4. The DNS lookup for relay.mira.test resolves to 198.51.100.77. The workstation
   uses source port 41011 to send an HTTP POST to /sync/notes on port 80.
5. Filter `http.request.uri == "/sync/notes"`, select the packet, then use
   Analyze > Follow > TCP Stream. Read the reconstructed client request.
6. Its JSON body identifies collection-copy and Base64. The parts arrive in
   application order 3,1,4,2; sort by seq and join the data strings as 1,2,3,4.
   Decode only the joined Base64, not HTTP headers or the whole JSON object.
7. The result contains `TVT{the_stream_kept_the_last_word}`.

If copying the JSON body into message.json, this local command decodes it:

```bash
python3 - <<'PY'
import json,base64
from pathlib import Path
obj=json.loads(Path('message.json').read_text())
encoded=''.join(p['data'] for p in sorted(obj['parts'],key=lambda p:p['seq']))
print(base64.b64decode(encoded,validate=True).decode())
PY
```

Organizer solver: `python3 solve.py dist/silent-connection.pcap`.
It reconstructs TCP byte positions and ignores identical retransmissions,
then parses HTTP and performs the application ordering and decoding.
It does not import the generator or use its plaintext constants.

The single retransmission is intentional and is not extra application data.
TCP sequence numbers and JSON sequence fields serve different purposes.
Record the DNS endpoint, HTTP request, followed stream, decoded receipt, and
wrong/correct CTFd submissions. Teammate independent solve pending.
