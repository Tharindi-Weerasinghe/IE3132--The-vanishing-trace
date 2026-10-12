#!/usr/bin/env python3
import csv
from datetime import timedelta
import hashlib
import io
from pathlib import Path
import re
import subprocess
import sys
import unittest
from zipfile import ZipFile
import solve

ROOT=Path(__file__).resolve().parent
PACKET=ROOT/"dist/stage04-evidence.zip"
FLAG="TVT{a_missing_minute_left_a_trace}"

class EvidenceTests(unittest.TestCase):
    def test_gap_and_reconstruction(self):
        r=solve.reconstruct(PACKET)
        self.assertEqual(r["minute"],"2026-09-29T09:16:00+00:00")
        self.assertEqual(r["event"]["file_id"],"F071")
        self.assertEqual(r["actor"],"msen")
        self.assertEqual(r["path"],"artifacts/K7D2.bin")
        self.assertEqual(r["flag"],FLAG)

    def test_independent_monitor_covers_whole_interval(self):
        with ZipFile(PACKET) as z:rows=solve.table(z,"logs/host-monitor.csv")
        times=[solve.utc(r["timestamp_utc"]) for r in rows]
        self.assertEqual(len(times),9)
        self.assertTrue(all(b-a==timedelta(minutes=1) for a,b in zip(times,times[1:])))
        self.assertTrue(all(r["state"]=="up" for r in rows))
        self.assertEqual([int(r["uptime_seconds"]) for r in rows],list(range(7200,7740,60)))

    def test_all_exports_link_to_valid_sessions_and_metadata(self):
        with ZipFile(PACKET) as z:
            sessions={r["session_id"]:r for r in solve.table(z,"logs/sessions.csv")}
            meta={r["file_id"]:r for r in solve.table(z,"filesystem-metadata.csv")}
            for e in solve.table(z,"logs/collection-activity.csv"):
                s=sessions[e["session_id"]];m=meta[e["file_id"]];t=solve.utc(e["timestamp_utc"])
                self.assertLessEqual(solve.utc(s["login_utc"]),t)
                self.assertLessEqual(t,solve.utc(s["logout_utc"]))
                self.assertEqual(e["timestamp_utc"],m["created_utc"])
                self.assertEqual(m["created_utc"],m["modified_utc"])
                b=z.read(m["recovered_path"])
                self.assertEqual(len(b),int(m["size_bytes"]))
                self.assertEqual(hashlib.sha256(b).hexdigest(),m["sha256"])

    def test_all_objects_open_with_their_correlated_password(self):
        found=[]
        with ZipFile(PACKET) as z:
            sessions={r["session_id"]:r for r in solve.table(z,"logs/sessions.csv")}
            meta={r["file_id"]:r for r in solve.table(z,"filesystem-metadata.csv")}
            for e in solve.table(z,"logs/collection-activity.csv"):
                key=solve.utc(e["timestamp_utc"]).strftime("%Y%m%d%H%M")+"_"+sessions[e["session_id"]]["actor"]
                with ZipFile(io.BytesIO(z.read(meta[e["file_id"]]["recovered_path"]))) as inner:
                    self.assertTrue(inner.getinfo("receipt.txt").flag_bits&1)
                    note=inner.read("receipt.txt",pwd=key.encode()).decode()
                    found+=re.findall(r"TVT\{[^}]+\}",note)
        self.assertEqual(found,[FLAG])

    def test_wrong_password_rejected(self):
        with ZipFile(PACKET) as z:
            with ZipFile(io.BytesIO(z.read("artifacts/K7D2.bin"))) as inner:
                with self.assertRaises(RuntimeError):inner.read("receipt.txt",pwd=b"wrong")

    def test_no_plaintext_flag_or_organizer_source_in_packet(self):
        expected={"START-HERE.txt","recovery-policy.txt","filesystem-metadata.csv",
                  "logs/archive-audit.log","logs/host-monitor.csv","logs/sessions.csv",
                  "logs/collection-activity.csv","artifacts/P2A8.bin","artifacts/B9F1.bin",
                  "artifacts/K7D2.bin","artifacts/R4M6.bin","artifacts/V3C5.bin"}
        with ZipFile(PACKET) as z:
            self.assertIsNone(z.testzip());self.assertEqual(set(z.namelist()),expected)
            for name in z.namelist():self.assertNotIn(FLAG.encode(),z.read(name))

    def test_offline_reference_solver(self):
        r=subprocess.run([sys.executable,str(ROOT/"solve.py"),str(PACKET)],check=True,capture_output=True,text=True)
        self.assertIn(FLAG,r.stdout)

    def test_packet_checksum(self):
        expected=(ROOT/"dist/SHA256SUMS.txt").read_text().split()[0]
        self.assertEqual(hashlib.sha256(PACKET.read_bytes()).hexdigest(),expected)

if __name__=="__main__":unittest.main(verbosity=2)
