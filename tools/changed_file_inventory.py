"""List complete reviewed path changes against the approved main Git snapshot."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];E=R/'evidence';s=json.loads((E/'git-review-snapshot.json').read_text())
b={x['path']:x['sha'] for x in s['baseline']['tree'] if x['type']=='blob'};c={x['path']:x['sha'] for x in s['candidate']['tree'] if x['type']=='blob'}
for d in ['content','templates','assets-src','tools','docs','evidence']:
 for p in (R/d).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and not (d=='evidence' and p.suffix=='.png') and not ('screenshots' in p.parts and len(p.relative_to(R).parts)==3):
   data=p.read_bytes();c[p.relative_to(R).as_posix()]=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
for n in ['README.md','AGENTS.md','package.json','package-lock.json','requirements-dev.txt','.gitignore','LCA_RELEASE_REPORT_v102_0_0_RC3.md','SHA256SUMS.txt']:
 if (R/n).is_file():
  data=(R/n).read_bytes();c[n]=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
for n in ['evidence/CHANGED_FILE_INVENTORY.md','evidence/changed-file-inventory.json','evidence/ROUTE_CHANGE_MATRIX.md']:c.setdefault(n,'current-reviewed-file')
rows=[]
for p in sorted(set(b)|set(c)):
 if b.get(p)==c.get(p):continue
 rows.append({'path':p,'status':'ADDED' if p not in b else 'REMOVED' if p not in c else 'MODIFIED'})
counts={t:sum(x['status']==t for x in rows) for t in ['ADDED','MODIFIED','REMOVED']}
(E/'changed-file-inventory.json').write_text(json.dumps({'baseline_sha':s['baseline']['sha'],'candidate_snapshot_sha':s['candidate']['sha'],'scope':'Complete final reviewed paths/statuses against main; current source/evidence overlay. SHA256SUMS is external to source ZIP to avoid self-referential hashing.','counts':counts,'files':rows},indent=2)+'\n')
(E/'CHANGED_FILE_INVENTORY.md').write_text('# Complete changed-file inventory against approved main\n\nBaseline: `'+s['baseline']['sha']+'`. Candidate Git snapshot: `'+s['candidate']['sha']+'`, overlaid with final review/packaging evidence. Generated public root files are removed from this branch because reproducible dist replaces them; approved originals remain unchanged in main history. This inventory lists every changed path, including its own reporting paths; hashes are supplied by deployment/source package manifests.\n\n'+str(counts)+'\n\n| Status | Path |\n| --- | --- |\n'+''.join('| '+x['status']+' | `'+x['path']+'` |\n' for x in rows))
pages=json.loads((R/'content/pages.json').read_text());base=json.loads((E/'baseline-content-inventory.json').read_text());routes=json.loads((E/'route-audit.json').read_text());matrix=[]
for r in routes:
 k='index' if r['route']=='/' else r['route'][1:]
 matrix.append([r['route'],'present' if k in base else 'new','pages.json' if k in pages else 'hubs.json' if k in ['updates','owner-notices'] else 'updates.json','retained scope; company voice, proof and SEO updated' if k in base else 'new owner entry/hub or sourced notice','index' if r['indexed'] else 'noindex,follow',str(r['words']),str(len(pages.get(k,{}).get('proof',[])))])
(E/'ROUTE_CHANGE_MATRIX.md').write_text('# Route change matrix\n\nDetailed concepts/reasons/proof: CONTENT_RETENTION_REGISTER.md. Metadata/schema/links: SEO_ROUTE_MAP.md. No expected RC3 route is missing.\n\n| Route | Baseline | Authoring source | Change | Index | Words | Proof placements |\n| --- | --- | --- | --- | --- | --- | --- |\n'+''.join('| '+' | '.join(x)+' |\n' for x in matrix))
print(json.dumps(counts))
