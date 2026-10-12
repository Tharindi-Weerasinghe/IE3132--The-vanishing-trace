#!/usr/bin/env python3
"""Organizer-only reference solver; needs steghide and Pillow on lab VM."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from zipfile import ZipFile
from PIL import Image

def solve(packet):
    if shutil.which('steghide') is None:raise RuntimeError('Requires steghide')
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        with ZipFile(packet) as z:z.extract('mira_photo.jpg',tmp)
        photo=tmp/'mira_photo.jpg'
        caption=str(Image.open(photo).getexif().get(270,''))
        match=re.search(r'without spaces = ([a-z]+)',caption)
        if not match:raise RuntimeError('No usable EXIF Image Description')
        output=tmp/'recovered.txt'
        subprocess.run(['steghide','extract','-sf',str(photo),'-xf',str(output),
                        '-p',match.group(1),'-f'],check=True,capture_output=True,text=True)
        return output.read_text()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('packet',nargs='?',default='dist/stage01-evidence.zip')
    print(solve(p.parse_args().packet))
