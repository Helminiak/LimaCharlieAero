"""Enforce the amended notice copy in rendered editorial surfaces."""
from html import unescape
from pathlib import Path
import re
from lxml import html

ADDENDUM = (Path(__file__).resolve().parents[1] / 'docs/redesign/REVIEW_RESOLUTION_ADDENDUM_1.md').read_text()
AMENDMENT = ADDENDUM.split('## Amendment 1a')[1]
GEARBOX = re.search(r'^"(FAA AD .+)"$', AMENDMENT, re.M)[1]
SUPERSEDED = re.findall(r'phrase "([^"]+)"', AMENDMENT)
TURBO = re.search(r'Regulatory sentence: "(.*)"', ADDENDUM)[1]
SOURCE = re.search(r'Source line: "(.*)"', ADDENDUM)[1]
CORRECTION = re.search(r'link: (https://www.federalregister.gov/\S+)', ADDENDUM)[1]


def check_notices(root):
    for file in sorted(root.rglob('*')):
        if file.suffix not in {'.html', '.xml', '.rss', '.atom', '.json', '.txt', '.webmanifest'}:
            continue
        raw = unescape(file.read_text())
        for phrase in SUPERSEDED:
            if phrase in raw:
                raise ValueError(f'{file.name}: superseded gearbox wording: {phrase}')
        for day in ('November 23, 2026', '2026-11-23'):
            if '2026-22-03' in raw and day in raw:
                raise ValueError(f'{file.name}: superseded turbo date: {day}')
    for slug in ('rotax-gearbox-notice', 'owner-notices', 'updates'):
        doc = html.parse(root / (slug + '.html'))
        if slug == 'rotax-gearbox-notice':
            selectors = ['//main//p[@class="lead"]', '//meta[@name="description"]/@content',
                         '//meta[@property="og:description"]/@content']
        else:
            selectors = ['//article[.//a[@href="/rotax-gearbox-notice"]]/p[2]']
        for selector in selectors:
            if doc.xpath(f'string({selector})') != GEARBOX:
                raise ValueError(f'{slug}: missing Amendment 1a text in {selector}')
    doc = html.parse(root / 'rotax-turbocharger-notice.html')
    if TURBO not in doc.xpath('//main//p/text()'):
        raise ValueError('Missing A1-02 regulatory sentence')
    if not doc.xpath('//li[a[contains(@href,"2026-22307.pdf")]]/following-sibling::li[1]/a[@href=$url]', url=CORRECTION):
        raise ValueError('Missing adjacent A1-02 correction link')
    if not doc.xpath('//p[@class="source-note" and text()=$source]', source=SOURCE):
        raise ValueError('Missing A1-02 source line')
