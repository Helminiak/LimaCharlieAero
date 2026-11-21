"""Exercise publication safeguards with independent faults in a disposable source tree."""
import copy
import http.client
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from urllib.parse import urlencode
from unittest.mock import patch
from PIL import Image

from build_common import ROOT
from cases import select_cases
from publication import publication_errors
import preview

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value))

checks = []

def rejected(name, operation, expected):
    try:
        operation()
    except (AssertionError, ValueError) as error:
        if expected not in str(error):
            raise
        checks.append({'test': name, 'injected_result': 'REJECTED', 'command': 'python3 tools/verify_publication.py', 'expected_failure': expected, 'observed_failure': str(error)})
    else:
        raise AssertionError('Fault passed: ' + name)

def build(root, *args, error=None, item=None):
    result = subprocess.run([sys.executable, 'tools/build.py', *args], cwd=root, capture_output=True, text=True)
    if error:
        assert result.returncode != 0 and error in result.stderr, result.stderr
        checks.append({'test': item, 'command': 'python3 tools/verify_publication.py',
                       'fixture_command': 'python3 tools/build.py', 'expected_failure': error,
                       'observed_failure': result.stderr.strip().splitlines()[-1],
                       'injected_result': 'REJECTED', 'exit': result.returncode})
    else:
        assert result.returncode == 0, result.stderr

def assert_hidden(root, record):
    assert not (root/(record['slug']+'.html')).exists(), 'editor standalone leak'
    assert record['title'] not in (root/'updates.html').read_text(), 'editor hub leak'
    assert record['slug'] not in (root/'sitemap.xml').read_text(), 'editor sitemap leak'

def edit_flags(root):
    file = root/'content/updates.json'
    rows = read(file)
    fixtures = [dict(rows[0], slug='editor-flag-'+flag, title='Private flag '+flag, **{flag:True})
                for flag in ('internal','placeholder')]
    write(file, rows + fixtures)
    with patch.object(preview, 'ROOT', root), ThreadingHTTPServer(('127.0.0.1',0),preview.Handler) as server:
        server.root = root/'dist'
        server.editor_enabled = True
        server.root_file = None
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            for row in fixtures:
                q = dict(row, token=preview.TOKEN, original_slug=row['slug'], operation='save',
                         title=row['title']+' edited', body='\n\n'.join(row['body']),
                         sources='\n'.join(row['sources']), asof='2026-11-21')
                flag = row['slug'].removeprefix('editor-flag-')
                del q[flag]  # the actual form does not contain the suppression flag
                c = http.client.HTTPConnection('127.0.0.1',server.server_port, timeout=120)
                try:
                    c.request('POST','/__editor',urlencode(q),{'Content-Type':'application/x-www-form-urlencoded'})
                    response = c.getresponse()
                    assert response.status == 303, response.read()
                finally:
                    c.close()
                saved = next(r for r in read(file) if r['slug']==row['slug'])
                assert saved[flag] is True and saved['title'] == q['title']
                assert_hidden(server.root, saved)
        finally:
            server.shutdown()
            thread.join()
    saved_rows = read(file)
    for row in saved_rows:
        if row['slug'].startswith('editor-flag-'):
            del row[row['slug'].removeprefix('editor-flag-')]
    write(file,saved_rows)
    build(root)
    for row in fixtures:
        rejected('X-09 dropped '+row['slug'], lambda: assert_hidden(root/'dist',row),'editor standalone leak')
    write(file,rows)

def case_model(records, subjects):
    candidate = copy.deepcopy(records[0])
    candidate.update(slug='synthetic-confirmed', title='Synthetic record', state='published',
                     owner_confirmation=True, sources=['Synthetic reference'])
    for stage in candidate['stages']:
        stage['text']='Confirmed synthetic '+stage['name']
    assert select_cases([candidate],subjects,False)==[candidate]
    for field,value,error in [('owner_confirmation','false','boolean'),('owner_confirmation',False,'confirmed facts'),
                              ('sources',[None],'source reference'),('sources',['  '],'source reference'),
                              ('status','In progress · pending manufacturer review','conflicts with stages')]:
        rejected('X-10 '+field+' '+repr(value),lambda:select_cases([{**candidate,field:value}],subjects,False),error)

def surfaces(root, cases):
    draft=copy.deepcopy(cases[0])
    draft.update(slug='unpublished-fixture-61b',title='Unique private title 61b')
    draft['stages'][0]['text']='Private stage narrative 61b.'
    records=[*cases,draft]
    write(root/'content/cases.json',records)
    build(root)
    out=root/'dist'
    domain=read(root/'content/site.json')['domain']
    urls={domain+('/' if f.name=='index.html' else '/'+f.stem) for f in out.glob('*.html')
          if f.stem not in {'404','card','about-credentials','thank-you'}}
    def clean():
        errors=publication_errors(out,records,urls)
        if errors:
            raise ValueError(', '.join(errors))
    clean()
    fixtures=[
        ('sitemap.xml','</urlset>',f'<url><loc>{domain}/other-route</loc></url></urlset>','Exact sitemap membership'),
        ('sitemap.xml','</urlset>',f'<url><loc>{domain}/{draft["slug"]}</loc></url></urlset>','Draft content'),
        ('index.html','property="og:description" content="','property="og:description" content="'+draft['title'],'Draft content'),
        ('index.html','name="twitter:title" content="','name="twitter:title" content="'+draft['title'],'Draft content'),
        ('our-work.html','"@graph": [','"@graph": [{"name":"'+draft['title']+'"},','Draft content'),
        ('updates.html','</main>','<p>'+draft['stages'][0]['text']+'</p></main>','Draft content'),
        ('search-index.json','',json.dumps([draft['title']]),'Draft content'),
        ('site.webmanifest','"short_name": "','"short_name": "'+draft['slug'],'Draft content'),
        ('robots.txt','User-agent:', '# '+draft['slug']+'\nUser-agent:', 'Draft content'),
    ]
    for name,needle,replacement,error in fixtures:
        file=out/name
        exists=file.exists()
        original=file.read_text() if exists else ''
        assert needle in original
        file.write_text(original.replace(needle,replacement,1))
        rejected('X-11 '+name+' '+needle,clean,error)
        if exists:file.write_text(original)
        else:file.unlink()
    clean()

def main():
    os.environ.update(CLOUDFLARE_CF_FETCH_ENABLED='false',WRANGLER_SEND_METRICS='false')
    with tempfile.TemporaryDirectory(prefix='v103-publication-') as tmp:
        root=Path(tmp)
        for directory in ('tools','templates','assets-src','content'):
            shutil.copytree(ROOT/directory,root/directory,ignore=shutil.ignore_patterns('__pycache__'))
        registry=read(root/'content/proof-assets.json')
        records=read(root/'content/cases.json')
        case_model(records,{r['id'] for r in registry})
        build(root)
        source=root/'tools/build_assets.py'
        original=source.read_text()
        source.write_text(original.replace("'work':'engine-cage-weld-repair-detail-800'",
                                           "'work':'tl-ultralight-designer-correspondence'"))
        build(root,item='X-07 social card',error='Ineligible presentation subject: tl-ultralight-designer-correspondence')
        source.write_text(original)
        pool=root/'assets-src/images/proof'
        loose=pool/'unregistered.webp'
        Image.new('RGB',(24,24)).save(loose)
        build(root,item='X-08 loose file',error='Unregistered proof source')
        loose.unlink()
        known=root/'assets-src'/registry[0]['asset'].removeprefix('assets/')
        original=known.read_bytes()
        Image.new('RGB',(24,24)).save(known,icc_profile=b'SYNTHETIC PRIVATE ICC TEXT')
        build(root,item='X-08 ICC',error='Raster metadata in '+known.name)
        known.write_bytes(original)
        edit_flags(root)
        surfaces(root,records)
    for value in ['/our-wrok','/,/our-wrok']:
        result=subprocess.run(['node','tools/performance.mjs','dist','--after-only'],cwd=ROOT,
            env={**os.environ,'LCA_PERF_ROUTES':value},capture_output=True,text=True)
        assert result.returncode and 'Unknown or duplicate performance route' in result.stderr
        checks.append({'test':'X-13 '+value,
                       'command':'LCA_PERF_ROUTES='+value+' node tools/performance.mjs dist --after-only',
                       'expected_failure':'Unknown or duplicate performance route',
                       'observed_failure':next(line for line in result.stderr.splitlines() if line.startswith('Error:')),'injected_result':'REJECTED','exit':result.returncode})
    receipt={'status':'PASS','negative_cases':checks}
    (ROOT/'evidence/redesign/negative-tests.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'{len(checks)} injected faults rejected; clean controls passed')

if __name__=='__main__':
    main()
