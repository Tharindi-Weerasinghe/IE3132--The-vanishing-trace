#!/usr/bin/env python3
"""Organizer tests: actual player packet, independent solver, common misreadings."""
import hashlib
import re
import subprocess
import sys
import unittest
from pathlib import Path
from zipfile import ZipFile
import build
import solve

ROOT=Path(__file__).resolve().parent
PACKET=ROOT/"dist/stage03-evidence.zip"

class ChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cipher,cls.key=solve.load_evidence(PACKET)

    def test_reference_vector(self):
        self.assertEqual(build.encrypt("ATTACKATDAWN","LEMON"),"LXFOPVEFRNHR")
        self.assertEqual(solve.decrypt("LXFOPVEFRNHR","LEMON"),"ATTACKATDAWN")

    def test_key_comes_from_catalogue_in_dispatch_order(self):
        self.assertEqual(self.key,"LANTERN")

    def test_full_plaintext_and_one_flag(self):
        text=solve.decrypt(self.cipher,self.key)
        self.assertEqual(text,build.PLAINTEXT)
        self.assertEqual(re.findall(r"TVT\{[^}]+\}",text),[build.FLAG])

    def test_common_wrong_keys_do_not_produce_a_flag(self):
        for key in ("TERNLAN","LAN","TERN","FIELD","RAIN","MOSS","DUSK"):
            with self.subTest(key=key):
                self.assertNotRegex(solve.decrypt(self.cipher,key),r"TVT\{[^}]+\}")

    def test_case_and_punctuation_do_not_consume_key(self):
        self.assertEqual(build.encrypt("A-a_1!B\nC","BC"),"B-c_1!C\nE")
        self.assertEqual(solve.decrypt("B-c_1!C\nE","BC"),"A-a_1!B\nC")

    def test_player_packet_has_only_expected_evidence(self):
        with ZipFile(PACKET) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(set(z.namelist()),set(build.player_files()))
            for name in z.namelist():
                data=z.read(name)
                self.assertNotIn(build.FLAG.encode(),data)
                self.assertNotIn(build.KEY.encode(),data)
        self.assertNotIn(build.FLAG,self.cipher)

    def test_offline_solver_cli(self):
        r=subprocess.run([sys.executable,str(ROOT/"solve.py"),str(PACKET)],
                         capture_output=True,text=True,check=True)
        self.assertIn(build.FLAG,r.stdout)

    def test_manifest_checksum(self):
        expected=(ROOT/"dist/SHA256SUMS.txt").read_text().split()[0]
        self.assertEqual(hashlib.sha256(PACKET.read_bytes()).hexdigest(),expected)

if __name__=="__main__":
    if not PACKET.exists():
        raise SystemExit("First run: python3 build.py")
    unittest.main(verbosity=2)
