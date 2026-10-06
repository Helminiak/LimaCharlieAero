"""Freeze the verified public output and check the exact extracted ZIP."""
from pathlib import Path
from datetime import date
import json,zipfile,hashlib,shutil,argparse
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive-dir',default=str(ROOT/'releases'));args=ap.parse_args()
 site=json.loads((ROOT/'content/site.json').read_text(encoding="utf-8"));manifest=json.loads((ROOT/'evidence/deployment-manifest.json').read_text(encoding="utf-8"));out=ROOT/'dist';name='LCA_SITE_'+site['release'].replace('.','_').replace('-','_')+'_DEPLOYABLE.zip';archive_dir=Path(args.archive_dir).resolve();archive_dir.mkdir(parents=True,exist_ok=True);dest=archive_dir/name
 actual={p.relative_to(out).as_posix():sha(p.read_bytes()) for p in out.rglob('*') if p.is_file()};assert actual==manifest,'Output changed since verification'
 for key in ['index.html','_headers','_redirects','404.html']:assert key in actual
 assert all(not (out/f).is_symlink() for f in actual),'No public symlinks'
 forbidden=['/workspace/','temporary-owner-note','temporary-internal','temporary-placeholder','__editor','BEGIN PRIVATE KEY','ghp_','sk_live_']
 for p in out.rglob('*'):
  if p.is_file() and p.suffix in ['.html','.js','.css','.txt','.xml']:
   text=p.read_text(encoding="utf-8")
   assert all(s not in text for s in forbidden),'Private/test material in '+str(p)
 d=date.fromisoformat(site['date'])
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted(actual):
   info=zipfile.ZipInfo(name,(d.year,d.month,d.day,0,0,0));info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(out/name).read_bytes(),compresslevel=9)
 extracted=ROOT/'verification-root'
 if extracted.exists():shutil.rmtree(extracted)
 extracted.mkdir()
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  assert set(z.namelist())==set(manifest)
  z.extractall(extracted)
 checked={p.relative_to(extracted).as_posix():sha(p.read_bytes()) for p in extracted.rglob('*') if p.is_file()};assert checked==actual,'Extraction hash mismatch'
 record={'status':'PASS','release':site['release'],'archive':str(dest),'archive_sha256':sha(dest.read_bytes()),'archive_bytes':dest.stat().st_size,'public_files':len(actual),'html_routes':sum(f.endswith('.html') for f in actual),'deployment_root':'index.html is at ZIP root; no enclosing folder','clean_extraction_hashes_match':True,'baseline_sha256':'e160c234b86aac2076db101c1b2e1acd27c46ed010866fd1aa6b21ff8214710a','extracted_root':str(extracted)}
 (ROOT/'evidence/packaging.json').write_text(json.dumps(record,indent=2)+'\n', encoding="utf-8", newline="\n");print(json.dumps(record))
if __name__=='__main__':main()
