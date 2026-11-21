"""Check the approved copy and the actual linked WebP pixels in both builds."""
from pathlib import Path
import hashlib
import json
import struct

from lxml import html
from PIL import Image

from redact_proof import MASKS

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = (ROOT / 'docs/redesign/REVIEW_RESOLUTION.md').read_text()


def check_copy(root):
    for slug, selector in (
        ('s-lsa-e-lsa-maintenance', '//aside[@class="limits"]/h2 | //aside[@class="limits"]/p'),
        ('rotax-gearbox-notice', '//main//p[@class="lead"]'),
        ('rotax-turbocharger-notice', '//main//p[@class="source-note"]'),
        ('rotax-gearbox-propeller-vibration', '//div[@class="pair"]/preceding-sibling::h2[1]'),
    ):
        doc = html.parse(root / (slug + '.html'))
        elements = doc.xpath(selector)
        assert len(elements) == (2 if slug == 's-lsa-e-lsa-maintenance' else 1), slug
        for element in elements:
            value = element.text_content()
            assert ('"' + value + '"' in AUTHORITY or '**' + value + '**' in AUTHORITY), (slug, value)
    vibration = html.parse(root / 'rotax-gearbox-propeller-vibration.html')
    captions = vibration.xpath('//div[@class="pair"]//figcaption')
    assert [c.text_content() for c in captions] == [
        'FIG. 01 A DynaVibe reading of 1.27 IPS.', 'FIG. 02 A DynaVibe reading of 0.04 IPS.']
    main = vibration.xpath('string(//main)')
    assert 'does not prove a paired repair result' in main
    assert 'after correction' not in main.lower() and '1.27 IPS →' not in main
    work = html.parse(root / 'our-work.html')
    if not work.xpath('//article[@class="case-story"]'):
        for value in [work.xpath('string(//title)'), work.xpath('string(//h1)'),
                      work.xpath('string(//main//p[@class="lead"])'),
                      work.xpath('string(//meta[@name="description"]/@content)')]:
            assert value and '"' + value + '"' in AUTHORITY, value
        home = html.parse(root / 'index.html')
        for tag, value in [('h2', 'From the hangar floor.'),
                           ('p', 'Readings, findings and records from real aircraft.'),
                           ('a', 'See more of our work')]:
            assert home.xpath('//main//' + tag + '[text()=$value]', value=value), value


def check_documents(root):
    doc = html.parse(root / 'e-props-dealer-support.html')
    for subject, (size, masks) in MASKS.items():
        href, = doc.xpath('//a[img[@data-subject=$subject]]/@href', subject=subject)
        file = root / href.lstrip('/')
        data = file.read_bytes()
        assert data[:4] == b'RIFF' and data[8:16] == b'WEBPVP8L'
        # Exactly one lossless image chunk, including its optional padding byte.
        length, = struct.unpack_from('<I', data, 16)
        assert len(data) == 20 + length + length % 2
        with Image.open(file) as image:
            assert image.size == size and image.n_frames == 1 and image.mode == 'RGB'
            for left, top, right, bottom in masks:
                crop = image.crop((left, top, right + 1, bottom + 1))
                assert crop.getcolors(1) == [(crop.width * crop.height, (228, 233, 237))], subject
        yield root.name + '/' + subject, {
            'linked_file': href, 'sha256': hashlib.sha256(data).hexdigest(),
            'native_size': size, 'uniform_masks': len(masks)}


if __name__ == '__main__':
    receipt = {}
    for build in ('dist', 'dist-preview'):
        check_copy(ROOT / build)
        receipt.update(check_documents(ROOT / build))
    dest = ROOT / 'evidence/redesign/privacy/document-mask-checks.json'
    dest.write_text(json.dumps(receipt, indent=2) + '\n')
    print('Binding copy, four full-size links and all 48 native mask rectangles verified.')
