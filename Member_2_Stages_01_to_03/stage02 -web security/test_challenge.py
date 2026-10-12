#!/usr/bin/env python3
from threading import Thread
import unittest
from urllib.request import urlopen
import json
from app import make_server, allowed_bind
from solve import solve

class Stage2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=make_server('127.0.0.1',0)
        cls.port=cls.server.server_port
        cls.thread=Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)
    def test_read_normal_record(self):
        with urlopen(f'http://127.0.0.1:{self.port}/record/1') as r:
            obj=json.loads(r.read())
        self.assertEqual(obj['owner'],'guest')
    def test_idor_illustrated(self):
        self.assertIn('LTX{never_trust_the_user_id}',solve(f'http://127.0.0.1:{self.port}'))
    def test_public_bind_rejected(self):
        self.assertFalse(allowed_bind('0.0.0.0'))
        self.assertFalse(allowed_bind('8.8.8.8'))
if __name__=='__main__':unittest.main(verbosity=2)
