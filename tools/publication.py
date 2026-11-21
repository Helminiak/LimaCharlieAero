"""Shared publication boundaries for proof rasters and post-build inspection."""
import html
import json
import re
from pathlib import Path
from xml.etree import ElementTree
from PIL import Image

RASTERS = {'.jpg', '.jpeg', '.png', '.ico', '.webp', '.avif', '.gif', '.tiff', '.bmp'}

def eligible_registry(registry, cases):
    used = {subject for case in cases for stage in case['stages'] for subject in stage['evidence']}
    return {key: row for key, row in registry.items() if not row.get('case_only') or key in used}

def require_clean_raster(path):
    with Image.open(path) as image:
        image.load()
        # These format fields describe pixels or decoding, never embedded profiles,
        # comments, camera data, XMP, or arbitrary PNG text.
        allowed = {'background', 'loop', 'duration', 'timestamp', 'sizes', 'transparency',
                   'jfif', 'jfif_version', 'jfif_unit', 'jfif_density', 'dpi'}
        extra = set(image.info) - allowed
        if image.getexif() or extra:
            raise ValueError(f'Raster metadata in {path.name}: {sorted(extra)}')

def publication_errors(root, records, expected_urls, preview=False):
    errors = []
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locations = [el.text for el in ElementTree.parse(root/'sitemap.xml').findall('s:url/s:loc', ns)]
    if sorted(locations) != sorted(expected_urls):
        errors.append('Exact sitemap membership')
    if preview:
        return errors
    private = {value for case in records if case['state'] == 'draft'
               for value in [case['slug'], case['title'], case.get('limits', ''),
                             *(s['text'] for s in case['stages'])] if value}
    for file in sorted(root.rglob('*')):
        if not file.is_file():
            continue
        name = file.relative_to(root).as_posix()
        try:
            raw = file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raw = ''
        # Decode HTML attributes/entities and JSON string escapes (including
        # escaped Unicode) before comparing actual case narrative and identifiers.
        raw = re.sub(r'\\u([\da-fA-F]{4})', lambda m: chr(int(m[1], 16)), raw)
        text = html.unescape(raw).replace(r'\"', '"').replace(r'\/', '/')
        if any(value in name or value in text for value in private):
            errors.append('Draft content in ' + name)
    return errors
