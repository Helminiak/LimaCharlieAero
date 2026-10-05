import hashlib,json,re,sys,zipfile,posixpath
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
archive=Path(sys.argv[1])
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(archive.read_bytes())=='e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a'
with zipfile.ZipFile(archive) as z:
 manifest=[{'path':i.filename,'size_bytes':i.file_size,'sha256':sha(z.read(i))} for i in z.infolist() if not i.is_dir()]
 assert len(manifest)==214 and sum(i['size_bytes'] for i in manifest)==14184009
 for i in manifest:
  b=(root/i['path']).read_bytes();assert b==z.read(i['path']);assert len(b)==i['size_bytes'] and sha(b)==i['sha256']
paths={i['path'] for i in manifest}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and p.relative_to(root).parts[0] not in ('docs','baselines') and p.name!='README.md'}
assert actual==paths,(actual-paths,paths-actual)
(out/'manifest.json').write_text(json.dumps({'archive_sha256':sha(archive.read_bytes()),'file_count':214,'total_bytes':14184009,'files':manifest},indent=2)+'\n')
redirects={l.split()[0]:l.split()[1] for l in (root/'_redirects').read_text().splitlines() if l.strip() and not l.startswith('#')}
refs=[]
class Parser(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for k in ('href','src','poster','data','action'):
   if a.get(k): refs.append((current,a[k]))
  for k in ('srcset','imagesrcset'):
   if a.get(k):refs.extend((current,v.strip().split()[0]) for v in a[k].split(',') if v.strip())
for current in sorted(paths):
 if not current.endswith(('.html','.css','.js','.webmanifest','.svg')):continue
 s=(root/current).read_text()
 if current.endswith(('.html','.svg')):Parser().feed(s)
 refs.extend((current,m.group(1)) for m in re.finditer(r'url\(\s*[\"\']?([^\)\"\']+)',s))
 if current.endswith('.js'):
  refs.extend((current,m.group(1)) for m in re.finditer(r'''["']([^"'\n]+\.(?:html|css|js|png|webp|jpg|svg|woff2?|pdf|vcf)(?:\?[^"']*)?)["']''',s))
 if current.endswith('.webmanifest'):
  refs.extend((current,i['src']) for i in json.loads(s).get('icons',[]))
missing=[];checked=0
for source,ref in refs:
 u=urlsplit(ref)
 if u.scheme or u.netloc or not u.path:continue
 target=posixpath.normpath(posixpath.join(posixpath.dirname(source),unquote(u.path))) if not u.path.startswith('/') else unquote(u.path).lstrip('/')
 route='/'+target
 for _ in range(8):
  if route not in redirects:break
  route=urlsplit(redirects[route]).path
 target=route.lstrip('/')
 checked+=1
 if not any(p in paths for p in (target,target+'.html',target.rstrip('/')+'/index.html' if target else 'index.html')):missing.append({'source':source,'reference':ref,'resolved':target})
result={'byte_comparison':'PASS','file_count':214,'total_bytes':14184009,'missing_files':[],'extra_website_files':[],'local_references_checked':checked,'missing_targets':missing,'scope':'HTML attributes and srcsets, CSS URLs, literal JS asset paths, webmanifest icons; external services and dynamic JS excluded'}
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
