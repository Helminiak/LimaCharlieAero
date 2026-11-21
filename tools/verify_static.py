from pathlib import Path
from lxml import html
from publication import publication_errors, RASTERS, require_clean_raster
from urllib.parse import urlsplit,unquote
import json,re,hashlib,posixpath,sys
R=Path(__file__).resolve().parents[1];root=R/(sys.argv[1] if len(sys.argv)>1 else 'dist');E=R/'.build-evidence'/root.name;E.mkdir(exist_ok=True)
routes=json.loads((E/'routes.json').read_text());files={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()};errors=[];checks=0;rows=[];titles=[];descs=[];refs=0
expected=set(re.findall(r'^([a-z0-9-]+\.html)$',(R/'docs/RC3_CODEX_MASTER_IMPLEMENTATION_PROMPT.md').read_text(),re.M))
def ck(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
from notice_checks import check_notices
try:
 check_notices(root)
except ValueError as error:
 ck(False, str(error))
expected.add('our-work.html')
ck({r['file'] for r in routes}==expected,'40 expected routes');ck(len(routes)==40,'route count');ck(files==json.loads((E/'deployment-manifest.json').read_text()),'frozen output manifest')
ck(not any(p.split('/')[0] in ['docs','baselines','tools','content','evidence','templates','assets-src'] for p in files),'source excluded from public output')
redirects={l.split()[0]:l.split()[1] for l in (root/'_redirects').read_text().splitlines() if l.strip() and not l.startswith('#')}
xml=(root/'sitemap.xml').read_text();repetition={x:[] for x in ['Owner information','Unsure where to start?','What happens next','Inspection context','diagnosis and serviceability require aircraft-specific evidence and applicable instructions']};voices={x:0 for x in ['Joe','Joseph','we','our','us','team','technician','shop','Lima Charlie Aero']}
actual_subjects=set()
registry=json.loads((R/'content/proof-assets.json').read_text())
cases=json.loads((R/'content/cases.json').read_text())
registration=re.compile(r'(?<![A-Za-z0-9])N[0-9]{1,5}[A-Z]{0,2}(?![A-Za-z0-9])',re.I)
preview=root.name=='dist-preview'
zero_public_cases = not preview and not any(c['state']=='published' for c in cases)
indexed_files = expected - {'404.html','thank-you.html','card.html','about-credentials.html'}
domain=json.loads((R/'content/site.json').read_text())['domain']
expected_urls = set() if preview else {domain + ('/' if f=='index.html' else '/'+Path(f).stem) for f in indexed_files}
for error in publication_errors(root, cases, expected_urls, preview):
 ck(False,error)
ck(True,'publication surfaces inspected')
for path in files:
 ck(not registration.search(path),'registration in filename '+path)
 if Path(path).suffix.lower() in RASTERS:
  try:require_clean_raster(root/path)
  except ValueError as error:ck(False,str(error))
  else:ck(True,'clean raster '+path)
for r in routes:
 d=html.parse(str(root/r['file']));main=d.xpath('//main')[0];text=' '.join(main.text_content().split());raw=(root/r['file']).read_text();key=Path(r['file']).stem;canonical='https://limacharlieaero.com'+r['route']
 actual_subjects.update(d.xpath('//img/@data-subject'))
 seen_assets=set()
 seen_subjects=set()
 for image in d.xpath('//img'):
  urls={image.get('src','')}
  variants=image.xpath('@srcset | ancestor::picture[1]//source/@srcset')
  urls.update(candidate.strip().split()[0] for srcset in variants for candidate in srcset.split(',') if candidate.strip())
  assets={files.get(url.lstrip('/'),url) for url in urls}
  subject=image.get('data-subject')
  ck(not assets.intersection(seen_assets) and (not subject or subject not in seen_subjects),
     f'{key} repeated image: {subject or image.get("src")}')
  seen_assets.update(assets)
  seen_subjects.add(subject)
 headings=[' '.join(h.text_content().split()).casefold() for h in d.xpath('//h2')]
 ck(len(headings)==len(set(headings)),key+' distinct H2')
 ck(not re.search(r'joseph.{0,12}the shop.{0,12}helminiak',raw,re.I),key+' founder name')
 ck(not registration.search(' '.join(d.xpath('//body//text()[not(parent::script)] | //@alt | //meta/@content | //@data-caption'))), key+' public registration')
 ck(not registration.search(d.xpath('string(//script[@type="application/ld+json"])')),key+' registration in schema')
 if not preview:ck('[OWNER' not in raw and 'PRIVATE PREVIEW:' not in raw,key+' public copy clean')
 else:ck('noindex' in d.xpath('string(//meta[@name="robots"]/@content)'),key+' preview noindex')
 for para in main.xpath('.//p'):
  ck(not re.search(r'[.!?]\s+[A-Z][\w -]+\s+/\s+[A-Z][\w -]+$', ' '.join(para.text_content().split())),key+' trailing section label')
 if key=='faq':
  inbound=json.loads((R/'tools/fixtures/rc3-faq.json').read_text())['questions']
  for anchor,question in inbound.items():
   ck(d.xpath('string(//details[@id=$anchor]/summary)',anchor=anchor)==question,'RC3 FAQ #'+anchor)
 if zero_public_cases:
  ck(not re.search(r'\beach\s+(?:case|example)\b',' '.join([text,*d.xpath('//meta/@content')]),re.I),key+' zero case copy')
 if key=='support-request':
  ck(bool(d.xpath('//form[@id="aircraft-intake-form"]//input[@type="email" and @required]')),'native email path')
  ck(bool(d.xpath('//details[@id="native-phone"]//form//input[@type="tel" and @required and @pattern]')),'native phone path')
 if key=='our-work':
  for case in cases:
   present=bool(d.xpath('//*[@id=$slug]',slug=case['slug']))
   ck(present==(preview or case['state']=='published'),'case visibility '+case['slug'])
 title=d.xpath('string(//title)');desc=d.xpath('//meta[@name="description"]/@content')[0];h1=d.xpath('//h1');can=d.xpath('//link[@rel="canonical"]/@href');og=d.xpath('//meta[@property="og:url"]/@content')
 ck(len(h1)==1,r['file']+' H1');ck(can==[canonical] and og==can,r['file']+' canonical/OG');ck((canonical+'</loc>' in xml)==r['indexed'],r['file']+' sitemap');ck(bool(title and desc),r['file']+' metadata');ck(d.xpath('//html/@lang')==['en'],r['file']+' language')
 if r['indexed']:titles.append(title);descs.append(desc)
 for phrase in ['Tell Joe','Contact Joe','Call Joe','Text Joe','Meet Joe','Joe reviews','owner-operated']:ck(phrase.lower() not in raw.lower(),r['file']+' banned '+phrase)
 for phrase in repetition:
  if phrase.lower() in text.lower():repetition[phrase].append(key)
 for phrase in voices:voices[phrase]+=len(re.findall(r'\b'+re.escape(phrase)+r'\b',text,re.I))
 ids=d.xpath('//@id');ck(len(ids)==len(set(ids)),r['file']+' unique IDs')
 for i in d.xpath('//img'):ck('alt' in i.attrib and int(i.get('width','0'))>0 and int(i.get('height','0'))>0,r['file']+' image semantics')
 graph=json.loads(d.xpath('//script[@type="application/ld+json"]/text()')[0])['@graph'];types=[g['@type'] for g in graph];gids=[g['@id'] for g in graph if '@id' in g];ck(len(gids)==len(set(gids)),r['file']+' schema IDs');ck('aggregateRating' not in raw and '"@type": "Review"' not in raw,r['file']+' no fabricated ratings');ck(any(g.get('url')==canonical for g in graph),r['file']+' schema URL')
 if key=='index':ck(all(x in types for x in ['Organization','LocalBusiness','WebSite','WebPage']),'home entity types')
 if key=='faq':ck('FAQPage' in types,'FAQ schema')
 if key=='joseph-helminiak-bio':ck('ProfilePage' in types and 'Person' in types,'bio schema')
 if key in {'services','aircraft-records-review','light-sport-prebuy-evaluation','light-sport-experimental-avionics','s-lsa-e-lsa-maintenance','e-props-dealer-support'} or (key.startswith('rotax-') and not key.endswith('-notice')):ck('Service' in types and 'BreadcrumbList' in types,key+' service schema')
 ck(any(g.get('@id')=='https://limacharlieaero.com/#business' and g.get('telephone')=='+19803821344' for g in graph),key+' stable business identity')
 if key=='index':ck('https://limacharlieaero.com/#organization' in gids,'stable organization identity')
 if key=='joseph-helminiak-bio':ck(any(g.get('@id')=='https://limacharlieaero.com/#joseph-helminiak' and g.get('worksFor',{}).get('@id')=='https://limacharlieaero.com/#business' for g in graph),'person worksFor business')
 if key in {'rotax-gearbox-notice','rotax-turbocharger-notice','start-with-the-symptom','prebuy-first-inquiry','planning-service-downtime'}:ck('Article' in types and 'BreadcrumbList' in types,key+' editorial schema')
 links=d.xpath('//@href|//@src|//@poster');links += [i.split()[0] for ss in d.xpath('//@srcset') for i in ss.split(',') if i.strip()]
 for link in links:
  u=urlsplit(link)
  if u.scheme or u.netloc or not u.path:continue
  refs+=1;t=unquote(u.path).lstrip('/') if u.path.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(r['file']),unquote(u.path)))
  for _ in range(8):
   if '/'+t not in redirects:break
   t=urlsplit(redirects['/'+t]).path.lstrip('/')
  ck(any(x in files for x in [t,t+'.html',t.rstrip('/')+'/index.html' if t else 'index.html']),r['file']+' missing '+link)
 rows.append({'route':r['route'],'indexed':r['indexed'],'title':title,'description':desc,'h1':h1[0].text_content(),'canonical':canonical,'words':len(text.split()),'schema':types,'links':sorted(set(d.xpath('//main//a/@href'))),'images':d.xpath('//main//img/@src')})
ck(len(titles)==len(set(titles)),'unique indexed titles');ck(len(descs)==len(set(descs)),'unique indexed descriptions')
for phrase,limit in zip(repetition,[3,10,12,5,2]):ck(len(repetition[phrase])<=limit,'repetition '+phrase)
# CSS asset references.
for path in root.glob('assets/*.css'):
 for target in re.findall(r'url\([\"\']?([^\)\"\']+)',path.read_text()):
  if not urlsplit(target).scheme:ck((path.parent/target).exists(),'CSS reference '+target)
proof=json.loads((R/'content/proof-assets.json').read_text());pages=json.loads((R/'content/pages.json').read_text());ck(50<=len(actual_subjects)<=55,'proof subject count');ck(all(x['permission'] in ['REVIEW REQUIRED','CLEARED'] for x in proof),'permission statuses explicit')
proof_by_id={x['id']:x for x in proof}
for key,p in pages.items():
 for image in p.get('proof',[]):
  a=proof_by_id.get(image['proof_id'],{})
  ck(a.get('asset')==image['src'] and bool(a.get('provenance')) and bool(image.get('caption')) and bool(image.get('alt')),key+' registered proof '+image['proof_id'])
permitted_case_images={i for c in cases if preview or c['state']=='published' for stage in c['stages'] for i in stage['evidence']}
ck(actual_subjects=={a['id'] for a in proof if not a.get('case_only') or a['id'] in permitted_case_images},'rendered subject coverage')
for key,min_count in {'index':4,'services':4,'rotax-gearbox-propeller-vibration':3,'rotax-installation-review':4,'rotax-fuel-pressure-fuel-delivery-problems':3,'light-sport-experimental-avionics':3,'e-props-dealer-support':3,'aircraft-records-review':1,'the-lima-charlie-aero-standard':3,'light-sport-prebuy-evaluation':1,'contact':1,'service-area':1,'joseph-helminiak-bio':1}.items():ck(len(pages[key].get('proof',[]))>=min_count,key+' proof placement')
result={'status':'PASS' if not errors else 'FAIL','checks':checks,'references':refs,'routes':len(rows),'proof_subjects':len(actual_subjects),'errors':errors,'repetition':repetition,'voice_frequency':voices,'rights_gate':'REVIEW REQUIRED — private candidate only; no public publication authorization inferred'}
(E/'static-checks.json').write_text(json.dumps(result,indent=2)+'\n');(E/'route-audit.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(errors))
