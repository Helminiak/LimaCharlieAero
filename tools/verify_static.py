from pathlib import Path
from lxml import html
from urllib.parse import urlsplit,unquote
import json,re,hashlib,posixpath,sys
R=Path(__file__).resolve().parents[1];root=R/(sys.argv[1] if len(sys.argv)>1 else 'dist');E=R/'evidence';E.mkdir(exist_ok=True)
routes=json.loads((E/'routes.json').read_text());files={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()};errors=[];checks=0;rows=[];titles=[];descs=[];refs=0
expected=set(re.findall(r'^([a-z0-9-]+\.html)$',(R/'docs/RC3_CODEX_MASTER_IMPLEMENTATION_PROMPT.md').read_text(),re.M))
def ck(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
ck({r['file'] for r in routes}==expected,'39 expected routes');ck(len(routes)==39,'route count');ck(files==json.loads((E/'deployment-manifest.json').read_text()),'frozen output manifest')
ck(not any(p.split('/')[0] in ['docs','baselines','tools','content','evidence','templates','assets-src'] for p in files),'source excluded from public output')
redirects={l.split()[0]:l.split()[1] for l in (root/'_redirects').read_text().splitlines() if l.strip() and not l.startswith('#')}
sitemap=html.parse(str(root/'sitemap.xml'));xml=(root/'sitemap.xml').read_text();repetition={x:[] for x in ['Owner information','Unsure where to start?','What happens next','Inspection context']};voices={x:0 for x in ['Joe','Joseph','we','our','us','team','technician','shop','Lima Charlie Aero']}
for r in routes:
 d=html.parse(str(root/r['file']));main=d.xpath('//main')[0];text=' '.join(main.text_content().split());raw=(root/r['file']).read_text();key=Path(r['file']).stem;canonical='https://limacharlieaero.com'+r['route']
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
 if key.startswith('rotax-') and not key.endswith('-notice'):ck('Service' in types and 'BreadcrumbList' in types,key+' service schema')
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
for phrase,limit in zip(repetition,[3,10,12,5]):ck(len(repetition[phrase])<=limit,'repetition '+phrase)
# CSS asset references.
for path in root.glob('assets/*.css'):
 for target in re.findall(r'url\([\"\']?([^\)\"\']+)',path.read_text()):
  if not urlsplit(target).scheme:ck((path.parent/target).exists(),'CSS reference '+target)
proof=json.loads((R/'content/proof-assets.json').read_text());pages=json.loads((R/'content/pages.json').read_text());ck(35<=len(proof)<=45,'proof subject count');ck(all(x['permission'] in ['REVIEW REQUIRED','CLEARED'] for x in proof),'permission statuses explicit')
for key,min_count in {'index':4,'services':4,'rotax-gearbox-propeller-vibration':3,'rotax-installation-review':4,'rotax-fuel-pressure-fuel-delivery-problems':3,'light-sport-experimental-avionics':3,'e-props-dealer-support':3,'aircraft-records-review':1,'the-lima-charlie-aero-standard':3,'light-sport-prebuy-evaluation':1,'contact':1,'service-area':1,'joseph-helminiak-bio':1}.items():ck(len(pages[key].get('proof',[]))>=min_count,key+' proof placement')
result={'status':'PASS' if not errors else 'FAIL','checks':checks,'references':refs,'routes':len(rows),'proof_subjects':len(proof),'errors':errors,'repetition':repetition,'voice_frequency':voices,'rights_gate':'REVIEW REQUIRED — private candidate only; no public publication authorization inferred'}
(E/'static-checks.json').write_text(json.dumps(result,indent=2)+'\n');(E/'route-audit.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(errors))
