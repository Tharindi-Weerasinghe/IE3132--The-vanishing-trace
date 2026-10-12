#!/usr/bin/env python3
"""INTENTIONALLY VULNERABLE toy IDOR for OFFLINE coursework lab only.

Not the group's real Flask app. Defaults to loopback and refuses public bindings.
Never expose this demonstration service to the Internet.
"""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from ipaddress import ip_address,ip_network
from urllib.parse import urlsplit
import argparse
import json

RECORDS={
  1: {'owner':'guest','content':'Guest entry: system check complete.'},
  2: {'owner':'guest','content':'Guest entry: train schedule.'},
  7: {'owner':'admin','content':'Private case receipt: LTX{never_trust_the_user_id}'},
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/':
            self.reply(200,{'message':'Mira record portal - local training server','help':'GET /record/1'})
            return
        if path.startswith('/record/') and path[8:].isdecimal():
            record=RECORDS.get(int(path[8:]))
            if not record:self.reply(404,{'error':'Record not found'});return
            # Deliberate IDOR for the contained challenge: checks ID exists but never
            # checks whether a guest is allowed to see that record. Do not reuse.
            self.reply(200,{'record_id':int(path[8:]),**record});return
        self.reply(404,{'error':'Not found'})
    def reply(self,status,obj):
        data=json.dumps(obj).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers();self.wfile.write(data)
    def log_message(self,fmt,*args):pass

def allowed_bind(host):
    ip=ip_address(host)
    return ip.is_loopback or ip in ip_network('192.168.128.0/24')

def make_server(host='127.0.0.1',port=5000):
    if not allowed_bind(host):raise ValueError('Use loopback or dedicated isolated 192.168.128.0/24 VM only')
    return ThreadingHTTPServer((host,port),Handler)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1')
    p.add_argument('--port',type=int,default=5000);a=p.parse_args()
    print('Local toy IDOR lab only; do not expose to Internet.')
    with make_server(a.host,a.port) as server:server.serve_forever()
