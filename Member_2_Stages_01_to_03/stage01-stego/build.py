#!/usr/bin/env python3
"""Reference JPEG/steghide builder for the isolated course lab (not team's original)."""
import hashlib
from pathlib import Path
import random
import shutil
import struct
import subprocess
import tempfile
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
from PIL import Image

ROOT=Path(__file__).resolve().parent
FLAG='LTX{mira_hidden_in_plain_sight}'
PASSPHRASE='aftertherain'


def make_cover(path):
    rng=random.Random(20260929)
    im=Image.new('RGB',(800,520))
    pixels=im.load()
    for y in range(520):
        for x in range(800):
            delta=rng.randrange(-20,21)
            pixels[x,y]=(max(0,min(255,70+y//5+delta)),
                         max(0,min(255,105+y//6+delta)),
                         max(0,min(255,130+y//8+delta)))
    im.save(path,'JPEG',quality=94,subsampling=0)


def add_exif_description_preserving_jpeg(jpg,description):
    """Inject APP1 EXIF without re-encoding JPEG's stego-bearing image data."""
    exif=Image.Exif()
    exif[270]=description  # ImageDescription
    data=exif.tobytes()
    if len(data)+2>65535:raise ValueError('EXIF too large')
    original=jpg.read_bytes()
    if not original.startswith(b'\xff\xd8'):raise ValueError('Not JPEG')
    app1=b'\xff\xe1'+struct.pack('>H',len(data)+2)+data
    jpg.write_bytes(original[:2]+app1+original[2:])
    caption=Image.open(jpg).getexif().get(270,'')
    if caption!=description:raise RuntimeError('EXIF was not preserved')


def main():
    if shutil.which('steghide') is None:
        raise SystemExit('Install steghide inside Kali lab first; this host cannot build Stage 01.')
    out=ROOT/'dist';out.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp)
        photo=temp/'cover.jpg';make_cover(photo)
        note=temp/'note.txt'
        note.write_text('Mira Sen / recovered field note\nEvidence receipt: '+FLAG+'\n',encoding='utf-8')
        final=out/'mira_photo.jpg'
        subprocess.run(['steghide','embed','-cf',str(photo),'-ef',str(note),'-sf',str(final),
                        '-p',PASSPHRASE,'-f'],check=True,capture_output=True,text=True)
        add_exif_description_preserving_jpeg(final,
            'Mira photo archive / Image Description: the phrase after the rain, joined without spaces = '+PASSPHRASE)
    player=out/'stage01-evidence.zip'
    instructions=("THE LAST TRANSMISSION / THE PHOTOGRAPHER'S SECRET\n"
        "The recovered JPEG has an archive description. Examine the metadata, "
        "then investigate whether the photograph carries anything else. "
        "Submit the receipt found in the hidden field note.\n")
    with ZipFile(player,'w',ZIP_DEFLATED) as z:
        for name,data in [('START-HERE.txt',instructions.encode()),('mira_photo.jpg',final.read_bytes())]:
            info=ZipInfo(name,(2026,9,29,10,0,0));info.compress_type=ZIP_DEFLATED
            z.writestr(info,data)
    (out/'SHA256SUMS.txt').write_text(hashlib.sha256(player.read_bytes()).hexdigest()+
                                     '  stage01-evidence.zip\n')
    print('Player packet:',player)

if __name__=='__main__':main()
