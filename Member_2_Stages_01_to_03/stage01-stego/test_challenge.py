#!/usr/bin/env python3
import hashlib
from pathlib import Path
import shutil
import unittest
from zipfile import ZipFile
from PIL import Image
import solve

ROOT=Path(__file__).resolve().parent
class Stage1Tests(unittest.TestCase):
    def test_generated_player_packet(self):
        packet=ROOT/'dist/stage01-evidence.zip'
        if not packet.exists():self.skipTest('Build on Kali with Pillow + steghide first')
        with ZipFile(packet) as z:
            self.assertEqual(set(z.namelist()),{'mira_photo.jpg','START-HERE.txt'})
            self.assertIsNone(z.testzip())
            self.assertNotIn(b'LTX{',z.read('START-HERE.txt'))
        digest=(ROOT/'dist/SHA256SUMS.txt').read_text().split()[0]
        self.assertEqual(hashlib.sha256(packet.read_bytes()).hexdigest(),digest)
    @unittest.skipUnless(shutil.which('steghide'),'steghide is required (run on Kali VM)')
    def test_reference_solver(self):
        packet=ROOT/'dist/stage01-evidence.zip'
        if not packet.exists():self.skipTest('Build player packet first')
        self.assertIn('LTX{mira_hidden_in_plain_sight}',solve.solve(packet))
if __name__=='__main__':unittest.main(verbosity=2)
