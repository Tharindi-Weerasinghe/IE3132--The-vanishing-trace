import unittest
from inspect_platform import analyze_routes
class RouteReviewTests(unittest.TestCase):
    def test_default_route_is_flagged(self):
        self.assertTrue(analyze_routes('default via 192.168.1.1 dev eth0\n')['default_route_present'])
    def test_no_default_is_not_proof_of_isolation(self):
        d=analyze_routes('192.168.128.0/24 dev eth0\n')
        self.assertFalse(d['default_route_present'])
        self.assertIn('verify',d['warning'])
if __name__=='__main__': unittest.main(verbosity=2)
