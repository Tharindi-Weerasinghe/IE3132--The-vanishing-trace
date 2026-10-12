# Stage 01 – The Photographer's Secret

## Challenge Overview

This stage focuses on steganography, a technique used to hide secret information inside digital images. Participants must investigate a JPEG image, examine its metadata, identify hidden clues, and extract the secret message to obtain the CTF flag.

## Technologies Used
- Python 3
- Pillow (Python Imaging Library)
- Steghide
- Kali Linux

## Challenge Implementation

The challenge uses Python to generate an image containing hidden information. Participants examine the image metadata and use Steghide to extract the concealed message.

## How to Run

Run the following commands in Kali Linux:

```bash
python3 build.py
python3 test_challenge.py
python3 solve.py dist/stage01-evidence.zip
```

## Testing and Validation

The challenge includes scripts for building, testing, and solving the steganography task. Testing should confirm that the hidden information can be extracted successfully and the expected flag can be recovered.

## Deployment and Reset

Upload only `dist/stage01-evidence.zip` to the CTF platform after successful testing. Keep source files and `SOLUTION.md` private.

To reset the challenge, restore the original player files and reset the challenge scoring on the CTF platform if required.

## Learning Outcome

This challenge helps participants develop practical skills in image analysis, metadata investigation, steganography, and hidden data extraction.
