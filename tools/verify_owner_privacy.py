"""Verify final public/preview metadata and owner-supplied proof images offline."""
import hashlib
import json
from pathlib import Path
from PIL import Image
from build_common import ROOT
from proof_privacy import REGISTRATION, SERIAL, check_ocr
from publication import require_clean_raster, RASTERS
from redact_proof import PROOF

def main():
    for path in (ROOT/'content').rglob('*.json'):
        text=json.dumps(json.loads(path.read_text()),ensure_ascii=False)
        if REGISTRATION.search(text) or SERIAL.search(text):
            raise ValueError('Private identifier in '+path.name)
    receipt={'content_json_files':len(list((ROOT/'content').rglob('*.json'))),'builds':{}}
    for build in ('dist','dist-preview'):
        root=ROOT/build
        paths=[p for p in root.rglob('*') if p.suffix.lower() in RASTERS]
        for p in paths:
            require_clean_raster(p)
        receipt['builds'][build]={'rasters_without_private_metadata':len(paths)}
    registry=json.loads((ROOT/'content/proof-assets.json').read_text())
    maps=[json.loads((ROOT/'.build-evidence'/b/'asset-map.json').read_text()) for b in receipt['builds']]
    rows={}
    for r in registry:
        asset=r['asset']
        path=ROOT/'assets-src'/asset.removeprefix('assets/')
        raw=path.read_bytes()
        for build,amap in zip(receipt['builds'],maps):
            assert raw==(ROOT/build/amap[asset].lstrip('/')).read_bytes(),r['id']
        with Image.open(path) as im:
            count=check_ocr(im)
        rows[r['id']]={'sha256':hashlib.sha256(raw).hexdigest(),'ocr_words':count}
    receipt['native_proof']=rows
    receipt['method']='Tesseract English, 2x Lanczos, sparse text. Each distinct native scanned once after byte comparison with both builds. Six new masks also manually inspected at 2x.'
    (ROOT/'evidence/redesign/privacy/owner-update-scan.json').write_text(json.dumps(receipt,indent=2)+'\n')
    p=ROOT/'evidence/redesign/privacy/redaction-v2.json'
    updated=json.loads(p.read_text())
    for subject in PROOF:
        assert updated[subject]['sha256']==rows[subject]['sha256']
        updated[subject]['ocr']={'registration_hits':0,'airframe_serial_hits':0,'contact_pattern_hits':0,'words_read':rows[subject]['ocr_words']}
    p.write_text(json.dumps(updated,indent=2)+'\n')

if __name__=='__main__':
    main()
