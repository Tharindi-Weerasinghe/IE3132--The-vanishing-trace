#!/usr/bin/env python3
import hashlib
import ipaddress
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from zipfile import ZipFile
from scapy.all import rdpcap,IP,TCP,UDP,DNS
import solve

ROOT=Path(__file__).resolve().parent
PCAP=ROOT/"dist/silent-connection.pcap"
FLAG="TVT{the_stream_kept_the_last_word}"

class CaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.packets=rdpcap(str(PCAP))

    def test_protocols_and_conversation_count(self):
        self.assertTrue(any(DNS in p for p in self.packets))
        starts=[p for p in self.packets if TCP in p and int(p[TCP].flags)==2]
        self.assertEqual(len(starts),24)
        self.assertEqual(len(solve.streams(PCAP)),48)

    def test_packet_times_are_ordered(self):
        times=[p.time for p in self.packets]
        self.assertEqual(times,sorted(times))

    def test_documentation_addresses_and_test_domains_only(self):
        allowed=[ipaddress.ip_network(n) for n in ("192.0.2.0/24","198.51.100.0/24")]
        for p in self.packets:
            for addr in (p[IP].src,p[IP].dst):
                self.assertTrue(any(ipaddress.ip_address(addr) in net for net in allowed))
            if DNS in p:self.assertTrue(p[DNS].qd.qname.rstrip(b".").endswith(b".test"))

    def test_checksums(self):
        for p in self.packets:
            ip=p[IP].copy();want=ip.chksum;del ip.chksum
            self.assertEqual(IP(bytes(ip)).chksum,want)
            layer=TCP if TCP in p else UDP
            want=p[layer].chksum
            ip=p[IP].copy();del ip[layer].chksum
            self.assertEqual(IP(bytes(ip))[layer].chksum,want)

    def test_http_lengths(self):
        for data in solve.streams(PCAP).values():
            head,body=data.split(b"\r\n\r\n",1)
            sizes=[int(line.split(b":",1)[1]) for line in head.split(b"\r\n") if line.startswith(b"Content-Length:")]
            self.assertEqual(sizes,[len(body)])

    def test_retransmission_and_application_order(self):
        packets=[p for p in self.packets if TCP in p and p[TCP].sport==41011 and bytes(p[TCP].payload)]
        sequences=[int(p[TCP].seq) for p in packets]
        self.assertLess(len(set(sequences)),len(sequences))
        data=solve.streams(PCAP)[("192.0.2.10",41011,"198.51.100.77",80)]
        obj=json.loads(data.split(b"\r\n\r\n",1)[1])
        self.assertEqual([p["seq"] for p in obj["parts"]],[3,1,4,2])

    def test_exact_recovered_flag(self):
        endpoints,note,flag=solve.recover(PCAP)
        self.assertEqual(flag,FLAG);self.assertEqual(note.count(FLAG),1)
        self.assertEqual(endpoints,("192.0.2.10",41011,"198.51.100.77",80))
        self.assertNotIn(FLAG.encode(),PCAP.read_bytes())

    def test_player_zip_and_checksums(self):
        with ZipFile(ROOT/"dist/stage05-evidence.zip") as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(set(z.namelist()),{"START-HERE.txt","silent-connection.pcap"})
            self.assertEqual(z.read("silent-connection.pcap"),PCAP.read_bytes())
        for line in (ROOT/"dist/SHA256SUMS.txt").read_text().splitlines():
            digest,name=line.split()
            self.assertEqual(hashlib.sha256((ROOT/"dist"/name).read_bytes()).hexdigest(),digest)

    def test_offline_solver_cli(self):
        r=subprocess.run([sys.executable,str(ROOT/"solve.py"),str(PCAP)],check=True,capture_output=True,text=True)
        self.assertIn(FLAG,r.stdout)

    @unittest.skipUnless(shutil.which("tshark"),"TShark not installed in this environment; run on Kali")
    def test_tshark_http_and_follow_stream(self):
        r=subprocess.run(["tshark","-n","-r",str(PCAP),"-Y",'http.request.uri == "/sync/notes"',"-T","fields","-e","tcp.stream"],check=True,capture_output=True,text=True)
        ids=r.stdout.strip().splitlines();self.assertEqual(len(ids),1)
        follow=subprocess.run(["tshark","-n","-r",str(PCAP),"-q","-z",f"follow,tcp,ascii,{ids[0]}"],check=True,capture_output=True,text=True)
        self.assertIn("POST /sync/notes",follow.stdout)
        self.assertIn('"parts"',follow.stdout)

if __name__=="__main__":unittest.main(verbosity=2)
