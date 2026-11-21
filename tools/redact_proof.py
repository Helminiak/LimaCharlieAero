"""Regenerate the two publication derivatives from the 3d48ea6 baseline export."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
# Inclusive native pixel coordinates. The packet repeats identifiers in running
# heads, figure legends, tables and footers on several overlapping sheets.
MASKS = {
    'eprops-install-checklist-preview-1200': ((1200, 760), [
        (144,191,542,286), (142,478,559,614), (660,228,1117,280),
        (660,321,1123,356), (660,576,1105,614),
        (146,137,580,155), (147,646,312,664), (663,305,886,323),
    ]),
    'eprops-engineering-packet-fanout-1200-clean': ((1200, 780), [
        (181,315,325,366), (828,507,1159,646),
        (178,243,313,299), (142,584,453,641), (366,131,531,158),
        (355,337,544,474), (349,497,549,546), (348,570,550,603),
        (640,122,863,153), (651,167,767,254), (587,288,784,520),
        (597,605,799,634), (854,177,1080,222), (844,286,1081,320),
        (828,316,1126,509), (858,651,1151,706),
    ]),
}

def redact(baseline):
    for name, (size, masks) in MASKS.items():
        src = baseline / 'assets/images/eprops/proof' / (name + '.webp')
        with Image.open(src) as original:
            if original.size != size:
                raise ValueError(f'Unexpected source dimensions for {name}')
            image = original.convert('RGB')
        draw = ImageDraw.Draw(image)
        for rect in masks:
            draw.rectangle(rect, fill='#e4e9ed')
        image.save(ROOT/'assets-src/images/proof'/(name+'.webp'), lossless=True, method=6)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    redact(parser.parse_args().baseline)
