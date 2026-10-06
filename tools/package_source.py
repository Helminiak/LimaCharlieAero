"""Create a deterministic source/evidence archive; verify every extracted payload byte."""
from pathlib import Path
from datetime import date
import json,zipfile,hashlib,tempfile,subprocess,argparse
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive-dir',default=str(R/'releases'));a=ap.parse_args();out=Path(a.archive_dir);out.mkdir(parents=True,exist_ok=True);site=json.loads((R/'content/site.json').read_text());d=date.fromisoformat(site['date']);files={}
 for dirname in ['content','templates','assets-src','tools','docs','evidence']:
  for p in sorted((R/dirname).rglob('*')):
   # Only legacy screenshot PNGs are omitted; PNG brand/build inputs are required.
   # The final ZIP verification receipt contains this archive's hash and is
   # external to its payload, as is the root SHA256SUMS checksum manifest.
   if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and not (dirname=='evidence' and (p.suffix=='.png' or p.name=='final-source-package-checks.json')):files[p.relative_to(R).as_posix()]=p.read_bytes()
 for n in ['README.md','AGENTS.md','package.json','package-lock.json','requirements-dev.txt','.gitignore']:files[n]=(R/n).read_bytes()
 if (R/'LCA_RELEASE_REPORT_v102_0_0_RC3.md').is_file():files['LCA_RELEASE_REPORT_v102_0_0_RC3.md']=(R/'LCA_RELEASE_REPORT_v102_0_0_RC3.md').read_bytes()
 manifest={n:sha(b) for n,b in sorted(files.items())};files['SOURCE_PACKAGE_MANIFEST.json']=(json.dumps({'algorithm':'SHA-256','scope':'All payload files except this self-describing manifest','files':manifest},indent=2)+'\n').encode()
 dest=out/'LCA_SITE_v102_0_0_RC3_SOURCE_AND_VERIFICATION.zip'
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(files.items()):
   i=zipfile.ZipInfo(n,(d.year,d.month,d.day,0,0,0));i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b,compresslevel=9)
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  for n,h in manifest.items():assert sha(z.read(n))==h
 print(json.dumps({'archive':str(dest),'sha256':sha(dest.read_bytes()),'files':len(files),'extracted_payload_hashes':'PASS'}))
if __name__=='__main__':main()
