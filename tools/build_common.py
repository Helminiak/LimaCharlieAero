from pathlib import Path
from string import Template
from urllib.parse import urlparse
from datetime import date
import json, hashlib, shutil, re, html, argparse
from PIL import Image
import io
ROOT = Path(__file__).resolve().parents[1]
E = lambda s: html.escape(str(s), quote=True)

def digest(d):
    return hashlib.sha256(d).hexdigest()

def safe_link(url):
    if not (url.startswith('/') and (not url.startswith('//')) or urlparse(url).scheme in ['https', 'mailto', 'tel', 'sms']):
        raise ValueError('Unsupported link: ' + url)
    return E(url)
