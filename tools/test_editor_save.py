"""Submit actual fixture editor forms, inspect persisted fields and rebuilt pages."""
from pathlib import Path
import json
import http.client
import sys
from urllib.parse import urlencode, urlsplit
from lxml import html

url = urlsplit(sys.argv[1])
records = Path('content/updates.json')
turbo = 'rotax-turbocharger-notice'
cases = [(r['slug'], {'title': r['title'] + ' edited'}) for r in json.loads(records.read_bytes())
         if r['slug'].startswith('editor-flag-')]
for reviewer in ('', 'Synthetic fixture reviewer'):
    cases.append((turbo, dict(reviewer=reviewer, last_review='2026-11-22')))
for slug, changes in cases:
    conn = http.client.HTTPConnection(url.hostname, url.port, timeout=120)
    try:
        conn.request('GET', '/__editor?slug=' + slug)
        form = html.fromstring(conn.getresponse().read()).forms[0]
        q = dict(form.form_values(), operation='save', asof='2026-11-22')
        q.update(changes)
        conn.request('POST', '/__editor', urlencode(q), {'Content-Type':'application/x-www-form-urlencoded'})
        response = conn.getresponse()
        assert response.status == 303, response.read()
        saved = next(r for r in json.loads(records.read_bytes()) if r['slug'] == slug)
        assert all(saved[k] == value for k, value in changes.items())
        if slug == turbo:
            conn.request('GET', '/' + slug)
            doc = html.fromstring(conn.getresponse().read())
            assert 'on November 22, 2026.' in doc.xpath('string(//p[@class="source-note"])')
            assert 'Source checked 2026-11-22' in doc.xpath('string(//main)')
            reviewers = doc.xpath('//p[starts-with(text(),"Reviewer: ")]/text()')
            assert reviewers == (['Reviewer: Synthetic fixture reviewer.'] if changes['reviewer'] else [])
            print('Turbo save 303, November 22 source check, reviewer', repr(saved['reviewer']))
    finally:
        conn.close()
