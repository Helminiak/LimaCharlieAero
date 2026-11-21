"""Exercise publication safeguards with independent faults in a disposable source tree."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from PIL import Image

from build_common import ROOT
from cases import select_cases
from editorial import select_editorial
from datetime import date
from notice_checks import check_notices, GEARBOX, SUPERSEDED, TURBO, SOURCE, CORRECTION
from html import escape
from publication import publication_errors

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
    subprocess.run(['node', 'tools/test_editor_save.mjs'], cwd=root, check=True)
    for row in fixtures:
        saved = next(r for r in read(file) if r['slug'] == row['slug'])
        assert saved[row['slug'].removeprefix('editor-flag-')] is True
        assert_hidden(root/'dist', saved)
    saved_rows = read(file)
    turbo = 'rotax-turbocharger-notice'
    saved_rows = [next(r for r in rows if r['slug'] == turbo) if row['slug'] == turbo else row for row in saved_rows]
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

def notice_faults(root):
    turbo = next(r for r in read(root/'content/updates.json') if r['slug'] == 'rotax-turbocharger-notice')
    def validate(record):
        return select_editorial([record], {}, date.fromisoformat(turbo['last_review']))[0]
    assert validate(turbo) == [turbo]
    for reviewer, note, diagnostic in [('   ', None, 'Reviewer must'), ('', True, 'Source note must'),
                                       (False, 'Source', 'Reviewer must'), ('', '  ', 'Source note must'),
                                       ('', None, 'Editorial record needs')]:
        record = dict(turbo, reviewer=reviewer, source_note=note)
        if reviewer == '' and note is None:
            del record['source_note']
        rejected(f'R-02 {reviewer!r}, {note!r}', lambda: validate(record), diagnostic)
    for preview in (False, True):
        build(root, *(['--preview'] if preview else []))
        out = root / ('dist-preview' if preview else 'dist')
        check_notices(out)
        def fault(name, filename, before, after, diagnostic):
            path = out/filename
            original = path.read_text()
            assert before in original
            path.write_text(original.replace(before, after, 1))
            try:
                rejected(f'{name} {out.name} {filename}', lambda: check_notices(out), diagnostic)
            finally:
                path.write_text(original)
        for phrase in SUPERSEDED:
            fault('A1-01', 'updates.html', '</main>', phrase+'</main>', 'superseded gearbox wording')
        for day in ('November 23, 2026', '2026-11-23'):
            fault('A1-02', 'rotax-turbocharger-notice.html', 'November 4, 2026', day, 'superseded turbo date')
        for slug in ('rotax-gearbox-notice', 'owner-notices', 'updates'):
            fault('A1-01', slug+'.html', '>'+escape(GEARBOX)+'</p>', '>Wrong.</p>', 'missing Amendment 1a')
        for attr in ('name="description"', 'property="og:description"'):
            start = attr + ' content="' + escape(GEARBOX)
            fault('A1-01', 'rotax-gearbox-notice.html', start, attr+' content="Wrong', 'missing Amendment 1a')
        for value, diagnostic in [(TURBO, 'A1-02 regulatory sentence'), (SOURCE, 'A1-02 source line'),
                                  (CORRECTION, 'adjacent A1-02 correction link')]:
            fault('A1-02', 'rotax-turbocharger-notice.html', value, 'Wrong', diagnostic)


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
        notice_faults(root)
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
