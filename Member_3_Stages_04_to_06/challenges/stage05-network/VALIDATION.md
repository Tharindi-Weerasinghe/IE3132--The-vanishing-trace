# Validation status

Source syntax was checked during preparation. Runtime generation and tests
could not run in the preparation environment because Scapy's import-time
network-interface inspection requires an unavailable socket capability.
No packet-generation, checksum, decryption, or GUI pass is claimed here.

On Kali run python3 build.py, then python3 test_challenge.py. The suite has ten
checks: protocol/conversation count; timestamp ordering; fictional address/name
scope; IP/TCP/UDP checksums; HTTP lengths; retransmission and application ordering;
exact recovered flag; player ZIP and hashes; reference solver CLI; and TShark
HTTP dissection plus Follow TCP Stream. The TShark test skips if it is absent.
Keep the actual output; report failures before uploading to CTFd.

After automated tests, manually open the capture in Wireshark and solve a copy
downloaded from CTFd. Test wrong/correct flags and 300-point scoring. A teammate
must independently solve and assess the proposed Moderate-Hard difficulty.
