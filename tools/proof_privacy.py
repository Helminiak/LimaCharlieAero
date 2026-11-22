"""Read publication derivatives with local OCR, without writing private text to receipts."""
from pathlib import Path
import io
import re
import subprocess
from PIL import Image

REGISTRATION = re.compile(r'\bN[0-9][0-9A-Z]{0,4}\b', re.I)
SERIAL = re.compile(r'\bTLUSA\s*\d+', re.I)

def check_ocr(image):
    scaled = image.resize((image.width*2, image.height*2), Image.Resampling.LANCZOS)
    data = io.BytesIO()
    scaled.save(data, 'PNG')
    result = subprocess.run(['tesseract','stdin','stdout','--psm','11'], input=data.getvalue(),
                            capture_output=True, check=True, timeout=90)
    text = result.stdout.decode()
    if REGISTRATION.search(text):
        raise ValueError('Registration pattern in proof OCR')
    if SERIAL.search(text):
        raise ValueError('Airframe serial in proof OCR')
    if re.search(r'[\w.+-]+@[\w.-]+\.\w{2,}|\+\d{2,3}[ -]\d{3}[ -]\d{3}[ -]\d{3}', text):
        raise ValueError('Contact details in proof OCR')
    return len(text.split())

if __name__ == '__main__':
    from redact_proof import PROOF, ROOT
    for subject in PROOF:
        with Image.open(ROOT/'assets-src/images/proof'/(subject+'.webp')) as im:
            print(subject, check_ocr(im), 'words checked')
