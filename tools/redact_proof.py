"""Regenerate privacy-safe document previews from an approved baseline export.
Usage: python3 tools/redact_proof.py /path/to/exported/baseline
No source documents are copied into the public output.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import sys
R=Path(__file__).resolve().parents[1];B=Path(sys.argv[1]);dest=R/'assets-src/images/proof'
# Coordinates are normalized against the inspected 1200px baseline previews.
specs={
'eprops-install-checklist-preview-1200':[(.12,.252,.45,.375),(.119,.63,.465,.805),(.55,.30,.93,.368),(.55,.423,.935,.468),(.55,.758,.92,.807)],
'eprops-engineering-packet-fanout-1200-clean':[(.152,.405,.27,.468),(.69,.65,.965,.827)]
}
for name,rects in specs.items():
 src=B/'assets/images/eprops/proof'/f'{name}.webp';im=Image.open(src).convert('RGB');d=ImageDraw.Draw(im)
 for x1,y1,x2,y2 in rects:d.rectangle((round(x1*im.width),round(y1*im.height),round(x2*im.width),round(y2*im.height)),fill='#e4e9ed')
 im.save(dest/f'{name}.webp','WEBP',quality=86,method=6)
